from rest_framework.decorators import api_view, permission_classes
from .models import Blog, BlogComment, Rate
from .serializers import BlogSerializer, BlogCommentSerializer, RateSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

@api_view(["POST", "GET"])
def blog_api_create(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            serializer = BlogSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "GET":
        blogs = Blog.objects.all().order_by("id")
        
        paginator = PageNumberPagination()
        paginator.page_size = 5

        result_page = paginator.paginate_queryset(blogs, request)
        serializer = BlogSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

@api_view(["GET", "PUT", "PATCH", "DELETE"])
def blog_api_detail(request, id):
    try:
        blog = Blog.objects.get(id=id)
    except Blog.DoesNotExist:
        return Response({"error": "Blog not found"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serializer = BlogSerializer(blog)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == "PUT":
        serializer = BlogSerializer(blog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "PATCH":
        serializer = BlogSerializer(blog, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "DELETE":
        blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST", "GET"])
def blog_comment(request, blog_id):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = BlogCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            comments = BlogComment.objects.filter(blog_id=blog_id, set=0)
            replyComments = BlogComment.objects.filter(blog_id=blog_id, set=1)
            replySerializer = BlogCommentSerializer(replyComments, many=True)
            serializer = BlogCommentSerializer(comments, many=True)
            return Response({
                "comments": serializer.data,
                "replyComments": replySerializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "GET":
        try:
            comments = BlogComment.objects.filter(blog_id=blog_id, set=0)
            replyComments = BlogComment.objects.filter(blog_id=blog_id, set=1)
        except BlogComment.DoesNotExist:
            return Response({"Errors": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = BlogCommentSerializer(comments, many=True)
        replySerializer = BlogCommentSerializer(replyComments, many=True)
        return Response({
            "comments": serializer.data,
            "replyComments": replySerializer.data
        }, status=status.HTTP_200_OK)



@api_view(["POST", "GET"])
def blog_api_rate(request, blog_id):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = RateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            rates = Rate.objects.filter(blog_id=blog_id)
            total = 0
            for r in rates:
                total += r.rate
            average = total / (len(rates))
            return Response({"average": average}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "GET":
        rates = Rate.objects.filter(blog_id=blog_id)
        total = 0
        for r in rates:
            total += r.rate
        average = total / (len(rates))
        return Response({"average": average}, status=status.HTTP_200_OK)