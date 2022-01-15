from django.urls import path
from django.contrib.auth import views as auth_view

from . import views


urlpatterns = [
    path('', views.welcome, name='home'),
    path('login/', views.app_login, name='login'),
    path('logout/', auth_view.LogoutView.as_view(), name='logout'),
    path('register/', views.app_register, name='register'),
]
