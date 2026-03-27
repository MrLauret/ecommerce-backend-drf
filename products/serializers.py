from .models import Brand, Category, Product
from rest_framework import serializers

allowed_extension = ["jpg", "jpeg", "png", "gif"]
max_size = 1 * 1024 * 1024

class ProductSerializer(serializers.ModelSerializer):
    image = serializers.JSONField()
    class Meta:
        model = Product
        fields = "__all__"

    def validate_image(self, files):
        if len(files) > 3:
            raise serializers.ValidationError("Vượt quá số lượng file!")
        for file in files:
            if file.rsplit(".", 1)[1].lower() not in allowed_extension:
                raise serializers.ValidationError("Sai định dạng file!")
        return files

class BrandSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    
    class Meta:
        model = Brand
        fields = ["id", "name", "products"]

class CategorySerializer(serializers.ModelSerializer):
    brands = BrandSerializer(many=True)
    products = ProductSerializer(many=True)
    class Meta:
        model = Category
        fields = ["id", "name", "brands", "products"]




        