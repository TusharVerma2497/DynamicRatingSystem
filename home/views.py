from django.shortcuts import render
from concurrent.futures import ThreadPoolExecutor
import urllib.request
from movies.models import movies
import time
import json
#from django import db
import requests
import csv
import threading
def home(request):
    return render(request,'home/home.html',{'title':'HOME'})

def about(request):
    return render(request,'home/about.html',{'title':'ABOUT'})

moviesDbObject=movies.objects
def aboutt(request):
    global moviesDbObject
    success=0
    error=0
    movieIDs=moviesDbObject.all().values_list('imdb_id', flat=True)
    #movieIDs=movieIDs[0:15]
    startTime=time.time()
    with ThreadPoolExecutor(max_workers=250) as executor:
        results = executor.map(load_url, movieIDs)
    endTime=time.time()-startTime
    print(endTime)
    with open('errors.csv', 'w+', newline='') as file:
        writer = csv.writer(file)
        for result in results:
            if(result.get('status')=='0'):
                writer.writerow([result.get('id'),result.get('error')])
                error=error+1
            else:
                moviesDbObject.filter(imdb_id=result.get('id')).update(cover_url=result.get('poster'))
                success=success+1
    print(str(success)+'=================================/////////////////////////////////-----------')
    print(str(error)+'=================================/////////////////////////////////-----------')
    return render(request,'home/about.html',{'title':endTime})


def load_url(id):
    id=Stringify(id)
    link='http://www.omdbapi.com/?i=tt'+id+'&apikey=45b52ea5'
    r=requests.get(link)
    data = json.loads(r.text)
    if (data['Response'] == 'True'):
        return({'id':id,'status':'1','poster':data['Poster']})
    else:
        return({'id':id,'status':'0','error':data['Error']})

def Stringify(id):
    id=str(id)
    length=len(id)
    if length<8:
        return "0"*(8-length)+id
    else:
        return id