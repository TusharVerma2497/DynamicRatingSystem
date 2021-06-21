from django.shortcuts import render
from .models import movies
from . import helper as movieHelper

def result(request):
    b=request.GET['keyword']
    movie_set=movieHelper.searchMovieFromIMDb(keyword=b.lower())
    return render(request,'movies/results.html',{'a':movie_set,'title':b})


def details(request, movie_id):
    movie=movieHelper.getMovieFromIMDb(movie_id = movie_id)
    if movie.has_key('full-size cover url'):
        movies.objects.filter(imdb_id = movie_id).update(cover_url = movie['full-size cover url'])
    return render(request,'movies/details.html',{'movie':movie,'title':movie['title']})
