from rest_framework import serializers
from .models import Blog, BlogComment, Rate

class BlogSerializer(serializers.ModelSerializer):
    time = serializers.TimeField(format="%-I:%M%p")
    date = serializers.DateField(format="%B %-d, %Y")
    author = serializers.CharField(source='author.username')
    class Meta:
        model = Blog
        fields = "__all__"

class BlogCommentSerializer(serializers.ModelSerializer):
    time = serializers.TimeField(format="%-I:%M%p", read_only=True)
    date = serializers.DateField(format="%B %-d, %Y", read_only=True)
    class Meta:
        model = BlogComment
        fields = "__all__"

class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = "__all__"