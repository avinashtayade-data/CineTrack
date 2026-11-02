from django.db import models

# Create your models here.


from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    release_year = models.IntegerField()
    description = models.TextField()
    rating = models.FloatField()


def __str__(self):
    return self.title

