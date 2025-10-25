# rpg_project/urls.py

from django.contrib import admin
from django.urls import path, include # Import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('game.urls')), # Include your game app's URLs
]