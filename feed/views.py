# Create your views here.
from doubleblind.feed.models import Post, Rating
from django.http import HttpResponse
from django.shortcuts import render_to_response
import twitter

def twitter_feed(request):
	#will need to be replaced 
	twitter = twitter.Api()
	post = twitter.GetPublicTimeLine[0]
	return render_to_response("feed.html",{'post':post})

