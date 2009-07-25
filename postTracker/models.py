from django.db import models
from doubleblind.twitterauth.models import UserProfile

class Post(models.Model):
	text = models.CharField(max_length=150)
	poster_name = models.CharField(max_length=30)
	poster_id = models.IntegerField()
	rating = models.ForeignKey(Rating)

class Rating(models.Model):
	score = models.IntegerField()
	rater = models.ForeignKey(UserProfile)

# Create your models here.
