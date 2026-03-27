from django.urls import path
from . import views

urlpatterns = [
    path("blogs/", views.blog_api_create, name="blog_create"),
    path("blogs/<int:id>/", views.blog_api_detail, name="blog_detail"),
    path("comments/<int:blog_id>/", views.blog_comment, name="blog_comment"),
    path("rates/<int:blog_id>/", views.blog_api_rate, name="rate"),
]