from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Brand, Category, Product
from .serializers import BrandSerializer, ProductSerializer, CategorySerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
import os
from django.conf import settings
from PIL import Image
import json

@api_view(["GET", "POST"])
def products_api(request):
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    productname = request.GET.get("productname")
    price = request.GET.get("price")
    category = request.GET.get("category")
    brand = request.GET.get("brand")
    if request.method == "GET":
        if min_price and max_price:
            products = Product.objects.filter(price__range=(min_price, max_price))
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        products = Product.objects.all()
        if productname:
            products = products.filter(productname__icontains=productname)
        if price:
            products = products.filter(price__lte=price)
        if category:
            products = products.filter(category_id=category)
        if brand:
            products = products.filter(brand_id=brand)
        paginator = PageNumberPagination()
        paginator.page_size = 6
        results = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)

        
    if request.method == "POST":
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_403_FORBIDDEN)
        data = request.data.copy()
        files = request.FILES.getlist("image")
        saved_filename = []
        for file in files:
            filename = file.name.replace(" ", "_")
            base, ext = os.path.splitext(filename)
            ext = ext.lower()
            save_folder = os.path.join(settings.MEDIA_ROOT, "products")
            os.makedirs(save_folder, exist_ok=True)
            original_path = os.path.join(save_folder, f"{base}{ext}")
            with open(original_path, "wb+") as dest:
                for chunk in file.chunks():
                    dest.write(chunk)
            saved_filename.append(f"{base}{ext}")
            img = Image.open(original_path)
            for size in [100, 200]:
                img_copy = img.copy()
                img_copy.thumbnail((size, size))
                resized_name = f"{size}_{base}{ext}"
                resize_path = os.path.join(save_folder, resized_name)
                img_copy.save(resize_path)

        data["image"] = json.dumps(saved_filename)
        if not data["brand"].isdigit():
            data["brand"], data["brand"] = Brand.objects.get_or_create(name=data["brand"]) # (obj, created)
        else:
            data["brand"] = Brand.objects.get(id=data["brand"])
        if not data["category"].isdigit():
            data["category"], data["category"] = Category.objects.get_or_create(name=data["category"])
        else:
            data["category"] = Category.objects.get(id=data["category"])
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors)

@api_view(["GET"])
def product_category_api(request):
    categories = Category.objects.prefetch_related("brands")
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
def product_brand_api(request):
    brands = Brand.objects.prefetch_related("products")
    serializer = BrandSerializer(brands, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_product_api(request, user_id):
    my_products = Product.objects.filter(author_id=user_id)
    serializer = ProductSerializer(my_products, many=True)
    for p in my_products:
        print(p.image)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["PATCH", "GET", "DELETE"])
def products_detail_api(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == "PATCH":
        formData = request.data
        files = request.FILES.getlist("image")
        imageDelete = formData["imageDelete"]
        saved_filename = []
        if len(imageDelete) > 0:
            product.image = [img for img in product.image if img not in imageDelete]
        for file in files:
            filename = file.name.replace(" ", "_")
            base, ext = os.path.splitext(filename)
            ext = ext.lower()
            original_path = os.path.join(settings.MEDIA_ROOT, "products", f"{base}{ext}")
            with open(original_path, "wb+") as dest:
                for chunk in file.chunks():
                    dest.write(chunk)
            saved_filename.append(f"{base}{ext}")
        formData["image"] = saved_filename
        for img in formData["imageDelete"]:
            file_path = os.path.join(settings.MEDIA_ROOT, img)
            if os.path.exists(file_path):   
                os.remove(file_path)
        formData = {key: value for key, value in formData.items() if value not in ("", None, "undefined", "null")}
        serializer = ProductSerializer(product, data=formData, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors)
    if request.method == "GET":
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == "DELETE":
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def home_product(request):
    products = Product.objects.all()[:6]
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["POST"])
def get_cart(request):
    cart = request.data
    products = []
    for prdId, qty in cart.items():
        products.append(Product.objects.get(id=prdId))
    serializer = ProductSerializer(products, many=True)
    for prd in serializer.data:
        for prd_id, qty in cart.items():
            if prd["id"] == int(prd_id):
                prd["qty"] = qty
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["POST"])
def wish_list(request):
    wishlist = request.data
    products = []
    try:
        for prd_id in wishlist:
            products.append(Product.objects.get(id=prd_id))
    except Product.DoesNotExist:
        return Response({"errors": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
def category_product(request):
    categories = Category.objects.prefetch_related("products")
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
def recommend_product(request):
    products = Product.objects.all()[:6]
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)