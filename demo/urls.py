from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import *

urlpatterns = [
    path("", catalog, name='catalog'),
    path("product/<product_pk>", product, name='product'),
    path("cart/", cart, name='cart'),
    path("orders/", orders, name='orders'),

    path("about/", about, name='about'),
    path("where/", where, name='where'),

    path("api/cart/add/<product_pk>", cart_add, name='cart_add'),
    path("api/cart/del/<product_pk>", cart_del, name='cart_del'),
    path("api/cart/checkout", cart_to_order, name='cart_to_order'),
    path("api/user/password", check_password, name='check_password'),

    path("register/", register.as_view(), name='register'),
    path("login/", LoginView.as_view(), name='login'),
    path("logout/", LogoutView.as_view(), name='logout')
]