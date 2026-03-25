from django.urls import path
from . import views

urlpatterns = [
    path("api/blogs/", views.blog_api_create, name="blog_create"),
    path("api/blogs/<int:id>/", views.blog_api_detail, name="blog_detail"),
    path("api/comments/<int:blog_id>/", views.blog_comment, name="blog_comment"),
    path("api/rates/<int:blog_id>/", views.blog_api_rate, name="rate"),
]