from django.db import models
from users.models import User

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)

class Brand(models.Model):
    name = models.CharField(max_length=200, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name="brands")

class Product(models.Model):
    productname = models.CharField(max_length=150)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, blank=True, null=True, related_name="products")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name="products")
    image = models.JSONField(default=list)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=100)
    sale = models.CharField(max_length=100, blank=True, null=True)
    detail = models.TextField()
    company = models.CharField(max_length=150)


