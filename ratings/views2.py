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
@login_required
def importRatings(request):
    if request.method=='POST':
        file=request.FILES['file-csv']
        csv=pd.read_csv(io.StringIO(file.read().decode('ISO-8859-1')),sep=',',names=['Const','YourRating','Date Rated','Title','URL','Title Type','IMDb Rating','Runtime (mins)','Year','Genres','Num Votes','Release Date','Directors'])
        csv=csv[['Const','YourRating','Date Rated']]
        for k,row in csv.iterrows():
            if row['Const']=='Const':continue
            if not movies.objects.filter(imdb_id=row['Const'][2:]).exists():
                t=threading.Thread(target=get_info,args=(row['Const'],row[1],row[2],request))
                l.append(t)
            else:
                data={
                    'score':row[1],
                    'movieId':row['Const'][2:],
                    'epoch':getEpoch(row[2]),
                    'userId':request.user.id,
                    'flag':2
                    }
                ratingHelper.insertRatingInDb(i = data, request = request)
        for i in l:
            i.start()
        for i in l:
            i.join()
        return redirect('rate')
    else:
        return redirect('rate')
    
def get_info(id,UserRating,dateRated,request):
    movie=movieHelper.getMovieFromOMDb(id=id)
    if (movie.get('Response') == 'True'):
        data={
            'id':id[2:],
            'title':movie.get('Title'),
            'year':movie.get('Year')[:4],
            'kind':movie.get('Type'),
            'cover url':movie.get('Poster'),
            'season':movie.get('Season'),
            'episode of':movie.get('Episode of'),
            'episode':movie.get('Episode')
            }
        movieHelper.insertMovieDataInDb(i=data)
        data={
            'score':UserRating,
            'movieId':id[2:],
            'epoch':getEpoch(dateRated),
            'userId':request.user.id,
            'flag':2
        }
        ratingHelper.insertRatingInDb(i = data, request = request)
   
def getEpoch(dateRated):
    b=dateRated.split('-')
    return datetime.datetime(int(b[0]),int(b[1]),int(b[2]),0,0,0,tzinfo=pytz.UTC).timestamp()