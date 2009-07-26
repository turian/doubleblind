from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.conf import settings

import friendfeed

import simplejson

def twitter_feed(request, user):
    """
    TODO: Want to get the user's timeline, not the public timeline.
    """
    import twitter
    twitterapi = twitter.Api()      # NOTE: This is an unauthenticated twitter
    import re
    usernamere = re.compile("@\S+")

    #timeline = twitterapi.GetFriendsTimeline(user, count=200)
    timeline = twitterapi.GetFriendsTimeline(user)
    #timeline = twitterapi.GetPublicTimeline()
    for status in timeline:
        status.blind_text = status.GetText()
        status.blind_text = usernamere.sub("@anonymous", status.blind_text)
    return render_to_response("feed.html", {"timeline": timeline}, context_instance=RequestContext(request))

_ffsession = None
def ffsession():
    global _ffsession
    if _ffsession is None:
        _ffsession = friendfeed.FriendFeed(settings.FRIENDFEED_NICKNAME, settings.FRIENDFEED_REMOTE_KEY)
    assert _ffsession is not None
    return _ffsession


def friendfeed_feed(request):
    """
    """
    fstr = simplejson.dumps(ffsession().fetch_favorites())
    #+ ffsession.fetch_public_feed()
    return render_to_response("feed.html", {"debug": [fstr]}, context_instance=RequestContext(request))
