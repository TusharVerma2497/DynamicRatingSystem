from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from unixtimestampfield.fields import UnixTimeStampField
from django.utils import timezone
from movies.models import movies

class rating(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    movie=models.ForeignKey(movies,on_delete=models.CASCADE)
    value=models.FloatField(null=False,blank=False,validators=[MaxValueValidator(10.0), MinValueValidator(0.1)])
    epoch=UnixTimeStampField(default=timezone.now)
    lastUpdated=UnixTimeStampField(default=timezone.now)
    class Meta:
        unique_together = ('user', 'movie',)

    def __str__(self):
        return "%s %s" % (self.user, self.movie)
