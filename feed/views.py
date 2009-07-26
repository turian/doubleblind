from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

import simplejson

import twitter
twitterapi = twitter.Api()      # NOTE: This is an unauthenticated twitter
                                # instance, we should use the OAuth information to authenticate

import re
usernamere = re.compile("@\S+")

def twitter_feed(request, user):
    """
    TODO: Want to get the user's timeline, not the public timeline.
    """
    #timeline = twitterapi.GetFriendsTimeline(user, count=200)
    #timeline = twitterapi.GetFriendsTimeline(user)
    timeline = twitterapi.GetPublicTimeline()
    for status in timeline:
        status.blind_text = status.GetText()
        status.blind_text = usernamere.sub("@anonymous", status.blind_text)
    return render_to_response("feed.html", {"timeline": timeline}, context_instance=RequestContext(request))

