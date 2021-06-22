from movies.models import movies
from ratings.models import rating
import memcache

mc = memcache.Client(['127.0.0.1:11211'],debug=0)

if not mc.get('globalVar-writingToDb'):
    mc.set('globalVar-writingToDb', 0)

if not mc.get('globalVar-m'):
    try:
        m = movies.objects.all().values('imdb_id')
        mc.set('globalVar-m', m)
    except Exception as e:
        print("not yet initialized")

if not mc.get('globalVar-semaphore'):
    mc.set('globalVar-semaphore', 0)




def getMoviesFromDb():
    while mc.get('globalVar-semaphore') > 150:
        pass
    mc.incr('globalVar-semaphore')
    while mc.get('globalVar-writingToDb') != 0:
        pass
    mc.decr('globalVar-semaphore')
    return mc.get('globalVar-m')



def insertBulkMoviesInDb(list):
    while mc.get('globalVar-semaphore') > 150:
        pass
    mc.incr('globalVar-semaphore')
    mc.incr('globalVar-writingToDb')
    movies.objects.bulk_create(list,ignore_conflicts=True)
    m = movies.objects.all().values('imdb_id')
    mc.set('globalVar-m', m)
    mc.decr('globalVar-writingToDb')
    mc.decr('globalVar-semaphore')

def insertBulkRatingsInDb(list):
    while mc.get('globalVar-semaphore') > 150:
        pass
    mc.incr('globalVar-semaphore')
    rating.objects.bulk_create(list,ignore_conflicts=True)
    mc.decr('globalVar-semaphore')

def getUserRatingsFromDb(userid):
    while mc.get('globalVar-semaphore') > 150:
        pass
    mc.incr('globalVar-semaphore')
    r=rating.objects.filter(user_id = userid)
    mc.decr('globalVar-semaphore')
    return r


def checkthenUpdateRating(obj):
    # while mc.get('globalVar-semaphore') > 150:
    #     pass
    pass
