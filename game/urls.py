# game/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.game_scene, name='game_scene'),
    path('scene/<str:scene_name>/', views.game_scene, name='game_scene_by_name'),
    path('choice/<str:scene_name>/<int:choice_index>/', views.make_choice, name='make_choice'),
]