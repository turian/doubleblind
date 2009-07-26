from django.db import models
from doubleblind.twitterauth.models import UserProfile

class Rating(models.Model):
	score=models.IntegerField()
	rater = models.ForeignKey(UserProfile)

class Poster(models.Model):
	name = models.CharField(max_length=50)
	id = models.IntegerField()
	raters = models.ManyToManyField(UserProfile)

class Post(models.Model):
	id = models.IntegerField()
	text = models.CharField(max_length=150)
	rating = models.ForeignKey(Rating)
	poster = models.ForeignKey(Poster)
	raters = models.ManyToManyField(UserProfile)


# Create your models here.

