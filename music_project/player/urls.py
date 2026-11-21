from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('delete/<int:song_id>/', views.delete_song, name='delete_song'),
    path('player/', views.music_player, name='music_player'),
    path('player/<int:song_id>/', views.music_player, name='music_player_song'),
]