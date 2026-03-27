from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    avatar = models.ImageField(upload_to="users", null=True, blank=True)
    sex = models.CharField(max_length=10)
    
    first_name=None
    last_name=None