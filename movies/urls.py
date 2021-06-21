from django.urls import path
from . import views


urlpatterns = [
    path('searchResults/', views.result,name='movie-result'),
    path('<int:movie_id>/detail/', views.details, name='movie-detail'),
]