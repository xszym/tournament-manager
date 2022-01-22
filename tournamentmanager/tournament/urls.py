from django.urls import path
from django.contrib.auth import views as auth_view

from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('login/', auth_view.LoginView.as_view(), name='login'),
    path('logout/', auth_view.LogoutView.as_view(), name='logout'),
    path('register/', views.app_register, name='register'),
]
