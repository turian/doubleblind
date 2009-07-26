from django.db import models
from doubleblind.twitterauth.models import UserProfile

class Rating(models.Model):
	score=models.IntegerField()
	post = models.ForeignKey("Post")
	rater = models.ForeignKey("Rater")

class Poster(models.Model):
	name = models.CharField(max_length=50)
	text = models.CharField(max_length=1000)

class Post(models.Model):
	post_id = models.CharField(max_length=60)
	text = models.CharField(max_length=1500)
	poster = models.ForeignKey(Poster)

class Rater(models.Model):
	host = models.CharField(max_length=75)

# Create your models here.

