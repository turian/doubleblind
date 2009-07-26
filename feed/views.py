from django.http import HttpResponse,HttpResponseRedirect
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
_last_creds = None
def ffsession(uname,rkey):
    """
    Cache the session with the last credentials.
    """
    global _ffsession, _last_creds
    creds = uname,rkey
    if _ffsession is None or _last_creds != creds:
        _ffsession = friendfeed.FriendFeed(uname, rkey)
        _last_creds = creds
    assert _ffsession is not None
    return _ffsession


def friendfeed_feed(request):
    """
    """
    if not (('username' in request.session) and ('remote_key' in request.session)):
#        uname = settings.FRIENDFEED_NICKNAME
#        rkey = settings.FRIENDFEED_REMOTE_KEY
        return HttpResponseRedirect("/login/")
    uname = request.session['username']
    rkey = request.session['remote_key']
    favs = ffsession(uname,rkey).fetch_favorites()
    blind_entries = []
    for e in favs["entries"]:
        btxt = e[u"body"]
        if "thumbnails" in e:
            btxt += "<br>"
            for t in e["thumbnails"]:
                # TODO: check that url and link don't contain "'"
                btxt += "<a href='%s'><img src='%s' width=%d height=%d></a>" % (t["link"], t["url"], t["width"], t["height"])
#        if "comments" in e:
#            btxt += "<table border=1><tr><td>Comments:</td></tr>"
#            for c in e["comments"]:
#                btxt += "<tr><td>%s</td></tr>" % c["body"]
#            btxt += "</table>"
#        import re
#        btxt = re.sub("lt", "gt", btxt)
        blind_entries.append(btxt)
    return render_to_response("feed.html", {"blind_entries": blind_entries}, context_instance=RequestContext(request))
#    return render_to_response("feed.html", {"blind_entries": blind_entries, "debug": simplejson.dumps(favs, indent=4)}, context_instance=RequestContext(request))
