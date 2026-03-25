from django.urls import path
from . import views

urlpatterns = [
    path("api/products/", views.products_api, name="product_list"),
    path("api/categories/", views.product_category_api, name="category"),
    path("api/categories/products/", views.category_product, name="category_product"),
    path("api/brands/", views.product_brand_api, name="brand"),
    path("api/products/<int:product_id>/", views.products_detail_api, name="product_detail"),
    path("api/users/<int:user_id>/products/", views.my_product_api, name="my_products"),
    path("api/home/", views.home_product, name="home_products"),
    path("api/carts/products/", views.get_cart, name="get_cart"),
    path("api/wishlists/products/", views.wish_list, name="wish_list"),
    path("api/recommend/products/", views.recommend_product, name="recommend_product")
]