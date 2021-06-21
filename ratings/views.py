from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from movies.models import movies
from .models import rating
import json
from movies import helper as movieHelper
from . import helper as ratingHelper
import pandas as pd
import threading
import datetime
import pytz
import io
from dynamicRatingSystem import globalVar

@login_required
def rate(request):
    if request.method == 'POST':
        data={
            'score':request.POST['rate'],
            'movieId':request.POST['movieId'],
            'epoch':float(request.POST['epoch']),
            'userId':request.user.id
        }
        ratingHelper.insertRatingInDb(request = request, i=data)
        dicts=ratingHelper.userRatingDataToDictionary(request = request)
        return render(request,'ratings/ratings.html',{'objs':json.dumps(dicts)})
    else:
        pass
    dicts=ratingHelper.userRatingDataToDictionary(request = request)
    return render(request,'ratings/ratings.html',{'objs':json.dumps(dicts)})


l=list()
movieObjects=list()
ratingObjects=list()
@login_required
def importRatings(request):
    global movieObjects
    global ratingObjects
    global l
    if request.method=='POST':
        file=request.FILES['file-csv']
        csv=pd.read_csv(io.StringIO(file.read().decode('ISO-8859-1')),sep=',',names=['Const','YourRating','Date Rated','Title','URL','Title Type','IMDb Rating','Runtime (mins)','Year','Genres','Num Votes','Release Date','Directors'])
        csv=csv[['Const','YourRating','Date Rated']]
        l=list()
        movieObjects=list()
        ratingObjects=list()
        moviesInDb = globalVar.getMoviesFromDb()
        userRatingsQuerySet = globalVar.getUserRatingsFromDb(request.user.id)
        userRatingsInDb = userRatingsQuerySet.values('movie_id')
        for k,row in csv.iterrows():
            if row['Const']=='Const':continue
            obj=rating(
                movie_id = row['Const'][2:],
                user_id = request.user.id,
                value = row[1],
                epoch = getEpoch(row[2]),
                lastUpdated = getEpoch(row[2]))
            if {'imdb_id':int(row['Const'][2:])} not in moviesInDb:
                t=threading.Thread(target=get_info,args=(row['Const'],row[1],row[2],request))
                l.append(t)
                ratingObjects.append(obj)
            else:
                if {'movie_id':int(row['Const'][2:])} not in userRatingsInDb:
                    ratingObjects.append(obj)
                else:
                    #globalVar.checkThenUpdateRating(obj)
                    m=userRatingsQuerySet.filter(movie_id = obj.movie_id)[0]
                    if m.value != obj.value and m.lastUpdated.timestamp() < obj.epoch:
                        rating.objects.filter(movie_id = obj.movie_id,user_id = request.user.id).update(value = obj.value, lastUpdated = obj.value)
                        print('Rating UPDATED-------------------------====================================000000000000000')
        for i in l:
            i.start()
        for i in l:
            i.join()
        l=list()
        globalVar.insertBulkMoviesInDb(movieObjects)
        globalVar.insertBulkRatingsInDb(ratingObjects)
        return redirect('rate')
    else:
        return redirect('rate')
    
def get_info(id,UserRating,dateRated,request):
    global movieObjects
    movie=movieHelper.getMovieFromOMDb(id=id)
    if (movie.get('Response') == 'True'):
        obj=movies(
            imdb_id=id[2:],
            title=movie.get('Title'),
            year=movie.get('Year')[:4],
            kind=movie.get('Type'),
            cover_url=movie.get('Poster'),
            episode_of=movie.get('Episode of'),
            season=movie.get('Season'),
            episode=movie.get('Episode'))
        movieObjects.append(obj)
   
def getEpoch(dateRated):
    b=dateRated.split('-')
    return datetime.datetime(int(b[0]),int(b[1]),int(b[2]),0,0,0,tzinfo=pytz.UTC).timestamp()