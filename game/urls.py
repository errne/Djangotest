# game/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.start_game, name='start_game'),
    path('new_game/', views.new_game, name='new_game'),
    path('game/', views.game_scene, name='game_scene'),
    path('game_over/', views.game_over, name='game_over'),
    path('choice/<str:scene_name>/<int:choice_index>/', views.make_choice, name='make_choice'),
    path('inventory/', views.inventory_view, name='inventory_view'),
    path('journal/', views.journal_view, name='journal_view'),
]