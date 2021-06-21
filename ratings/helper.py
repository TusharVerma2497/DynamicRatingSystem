from django.contrib.auth.decorators import login_required
from movies.models import movies
from .models import rating

ratingPresentInDb=rating.objects.filter


@login_required    
def insertRatingInDb(request, i):
    score = i.get('score')
    movieId = i.get('movieId')
    epoch = i.get('epoch')
    userId = i.get('userId')
    flag = i.get('flag')#this is needed only when inserting movies from ratings.csv since then epoch value is also inserted
    row = ratingPresentInDb(movie_id = movieId, user_id = userId)
    if not row.exists():
        if flag == 2:
            r = rating(movie_id = movieId, user_id = userId, value = score, epoch = epoch,lastUpdated = epoch)
        else:
            r = rating(movie_id = movieId, user_id = userId, value = score)
        r.save()
    elif row[0].value != score and row[0].lastUpdated.timestamp() < epoch:
        ratingPresentInDb(movie_id = movieId,user_id = userId).update(value = score,
        lastUpdated = epoch)
    else:
        pass



@login_required
def userRatingDataToDictionary(request):
    data = list(request.user.rating_set.all().order_by('-value','-epoch'))
    name = list()
    ratings = list()
    id = list()
    url = list()
    for i in data:
        # name.append(i.movie.title+" | "+str(i.movie.year)+" | "+i.movie.kind+" | "+str(i.epoch))
        name.append(i.movie.title+" | "+str(i.movie.year)+" | "+i.movie.kind)
        ratings.append(i.value)
        id.append(i.movie.imdb_id)
        url.append(i.movie.cover_url)
    return {'name':name,'rating':ratings,'id':id,'url':url}
