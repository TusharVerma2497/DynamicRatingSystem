from django.db import models

class movies(models.Model):
    imdb_id=models.PositiveIntegerField(primary_key=True)
    title=models.CharField(max_length=220,null=False,blank=False)
    year=models.PositiveSmallIntegerField(blank=True, null=True)
    kind=models.CharField(max_length=15,null=True,blank=False)
    cover_url=models.URLField(max_length = 500)
    episode_of=models.CharField(max_length=50,null=True,blank=False)
    season=models.PositiveSmallIntegerField(null=True)
    episode=models.PositiveSmallIntegerField(null=True)

    def __str__(self):
        return self.title
