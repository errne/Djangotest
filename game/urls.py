# game/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.game_scene, name='game_scene'),
    path('north/', views.north_path, name='north_path'), # Example for another path
    # Add more paths as your game grows
]