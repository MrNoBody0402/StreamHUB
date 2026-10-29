from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('watch/<str:media_type>/<int:tmdb_id>/', views.watch, name='watch'),
    path('actor/<int:person_id>/', views.actor_detail, name='actor_detail'),
    path('api/actor/<int:person_id>/works/', views.actor_works_api, name='actor_works_api'),
    path('api/recommendations/<str:media_type>/<int:tmdb_id>/', views.media_recommendations_api, name='media_recommendations_api'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('api/search/', views.search_suggestions, name='search_suggestions'),
]