from django.urls import path
from django.contrib.auth import views as auth_view
from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('login/', auth_view.LoginView.as_view(), name='login'),
    path('logout/', auth_view.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('tournaments/', views.TournamentListView.as_view(), name='tournaments_list'),
    path('create-tournament/', views.CreateTournamentView.as_view(), name='create_tournament'),
    path('create-team/' , views.CreateTeamView.as_view(), name='create_team'),
    path('teams/', views.TeamListView.as_view(), name='teams_list'),
]
