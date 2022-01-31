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
    path('team-tournament-request/' , views.CreateTeamTournamentRequestView.as_view(), name='team_tournament_request'),
    path('join-team-request/<slug:slug>', views.RequestTeamJoinView.as_view(), name='join_team_request'),
    path('change-join-team-request-status/<int:request_id>/<str:new_status>', views.change_JoinTeamRequest_status, name='change_join_team_request_status'),
    path('tournament-manage/' , views.TournamentManageView.as_view(), name='tournament_manage'),
    path('change-team-request-status/<int:request_id>/<str:new_status>/', views.change_TeamTournamentRequest_status, name='change_TeamTournamentRequest_status'),
    path('team/<slug:slug>/', views.TeamDetailsView.as_view(), name='team_details'),
    path('tournament/<slug:slug>/', views.TournamentDetailsView.as_view(), name='tournament_details'),
    path('tournament-generate-matches/<slug:slug>/', views.generate_matches, name='generate_matches'),
]
