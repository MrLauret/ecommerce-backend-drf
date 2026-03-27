from django.urls import path
from . import views

urlpatterns = [
    path("products/", views.products_api, name="product_list"),
    path("categories/", views.product_category_api, name="category"),
    path("categories/products/", views.category_product, name="category_product"),
    path("brands/", views.product_brand_api, name="brand"),
    path("products/<int:product_id>/", views.products_detail_api, name="product_detail"),
    path("users/<int:user_id>/products/", views.my_product_api, name="my_products"),
    path("home/", views.home_product, name="home_products"),
    path("carts/products/", views.get_cart, name="get_cart"),
    path("wishlists/products/", views.wish_list, name="wish_list"),
    path("recommend/products/", views.recommend_product, name="recommend_product")
]