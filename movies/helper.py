from imdb import IMDb
from memorised.decorators import memorise
from .models import movies
from ratings.models import rating
from django.contrib.auth.decorators import login_required
import json, requests


moviesPresentInDb=movies.objects.filter
imdbObject=IMDb()

@memorise(ttl=60*25)
def getMovieFromIMDb(movie_id):
    return(imdbObject.get_movie(movie_id))

    

@memorise(ttl=60*25)
def getMovieFromOMDb(id):
    link='http://www.omdbapi.com/?i='+id+'&apikey=45b52ea5'
    r=requests.get(link)
    return(json.loads(r.text))



@memorise(ttl=60*25)
def searchMovieFromIMDb(keyword):
    searchResults=imdbObject.search_movie(keyword)
    for i in searchResults:
        data={
            'id':i.getID(),
            'year':i.get('year'),
            'kind':i.get('kind'),
            'title':i.get('title'),
            'cover url':i.get('cover url'),
            'episode of':i.get('episode of'),
            'season':i.get('season'),
            'episode':i.get('episode')}
        insertMovieDataInDb(i=data)
    return searchResults



def insertMovieDataInDb(i):
    if not moviesPresentInDb(imdb_id=i.get('id')).exists():
        movie=movies(
            imdb_id=i.get('id'),
            title=i.get('title'),
            year=i.get('year'),
            kind=i.get('kind'),
            cover_url=i.get('cover url'),
            episode_of=i.get('episode of'),
            season=i.get('season'),
            episode=i.get('episode'))
        movie.save()



# @login_required    
# def insertRatingInDb(request, i):
#     score = i.get('score')
#     movieId = i.get('movieId')
#     epoch = i.get('epoch')
#     userId = i.get('userId')
#     flag = i.get('flag')#this is needed only when inserting movies from ratings.csv since then epoch value is also inserted
#     row = ratingPresentInDb(movie_id = movieId, user_id = userId)
#     if not row.exists():
#         if flag == 2:
#             r = rating(movie_id = movieId, user_id = userId, value = score, epoch = epoch,lastUpdated = epoch)
#         else:
#             r = rating(movie_id = movieId, user_id = userId, value = score)
#         r.save()
#     elif row[0].value != score and row[0].lastUpdated.timestamp() < epoch:
#         ratingPresentInDb(movie_id = movieId,user_id = userId).update(value = score,
#         lastUpdated = epoch)
#     else:
#         pass



# @login_required
# def userRatingDataToDictionary(request):
#     data = list(request.user.rating_set.all().order_by('-value','-epoch'))
#     name = list()
#     ratings = list()
#     id = list()
#     url = list()
#     for i in data:
#         # name.append(i.movie.title+" | "+str(i.movie.year)+" | "+i.movie.kind+" | "+str(i.epoch))
#         name.append(i.movie.title+" | "+str(i.movie.year)+" | "+i.movie.kind)
#         ratings.append(i.value)
#         id.append(i.movie.imdb_id)
#         url.append(i.movie.cover_url)
#     return {'name':name,'rating':ratings,'id':id,'url':url}



