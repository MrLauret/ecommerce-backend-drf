from django.db import models
from users.models import User
from django.utils import timezone

class Blog(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    time = models.TimeField(default=timezone.now)
    date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to="blogs")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blogs")

class BlogComment(models.Model):
    blog_id = models.IntegerField()
    user_id = models.IntegerField()
    user_name = models.CharField(max_length=150)
    comment_id = models.IntegerField()
    set = models.IntegerField()
    content = models.TextField()
    user_image = models.CharField(max_length=150)
    created_at=models.DateTimeField(auto_now_add=True, blank=True, null=True)
    time=models.TimeField(auto_now_add=True, blank=True, null=True)
    date=models.DateField(auto_now_add=True, blank=True, null=True)

class Rate(models.Model):
    user_id = models.IntegerField()
    blog_id = models.IntegerField()
    rate = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)