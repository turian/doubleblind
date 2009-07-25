# Create your views here.
from doubleblind.feed.models import Post, Rating
from django.http import HttpResponse

def twitter_feed(request):
	return HttpResponse("feed") 

