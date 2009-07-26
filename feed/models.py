from django.db import models
from doubleblind.twitterauth.models import UserProfile

class Rating(models.Model):
	time = models.DateTimeField(auto_now=True)
	score= models.IntegerField()
	entry = models.ForeignKey("Entry")
	rater = models.ForeignKey("Rater")

class Poster(models.Model):
	name = models.CharField(max_length=50)
	text = models.CharField(max_length=1000)

class Entry(models.Model):
	post_id = models.CharField(max_length=60)
	text = models.CharField(max_length=5000)
	poster = models.ForeignKey(Poster)

class Rater(models.Model):
	name = models.CharField(max_length=75)
	email = models.CharField(blank=True,max_length=100)
	remote_key = models.CharField(max_length=100,blank=True)
	has_been_prompted = models.BooleanField(default=False)

# Create your models here.

