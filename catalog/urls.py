from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('watch/<str:media_type>/<int:tmdb_id>/', views.watch, name='watch'),
    path('actor/<int:person_id>/', views.actor_detail, name='actor_detail'),
    path('watchlist/', views.watchlist, name='watchlist'),
]