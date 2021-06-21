from django.urls import path,include
from . import views


urlpatterns=[
    path('',views.rate,name='rate'),
    path('importRatings/',views.importRatings,name='importRatings'),
    ]