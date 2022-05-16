from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import *

urlpatterns = [
    path("", catalog, name='catalog'),
    path("about/", about, name='about'),
    path("where/", where, name='where'),
    path("register/", register.as_view(), name='register'),
    path("login/", LoginView.as_view(), name='login'),
    path("logout/", LogoutView.as_view(), name='logout')
]