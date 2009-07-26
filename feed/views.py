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

def add_vote(request, entry_index, rating):
    """
    TODO: This shouldn't be in views
    """
    if 'votes' not in request.session:
        request.session['votes'] = {}

    # TODO: Don't hardcode these URL names
    if rating == "thumbsup":
        request.session['votes'][entry_index] = +1
    elif rating == "thumbsdown":
        request.session['votes'][entry_index] = -1
    elif rating == "pass":
        request.session['votes'][entry_index] = None
    else:
        # TODO: Return 404
        assert 0

def friendfeed_vote(request, entry_index=None, rating=None):
    """
    """
    if entry_index is not None:
        # TODO: Fail gracefully if not an int
        entry_index = int(entry_index)
        add_vote(request, entry_index-1, rating)
    else:
        entry_index = 0

    # TODO: Store previous rating

    if not (('username' in request.session) and ('remote_key' in request.session)):
#        uname = settings.FRIENDFEED_NICKNAME
#        rkey = settings.FRIENDFEED_REMOTE_KEY
        return HttpResponseRedirect("/login/")
    uname = request.session['username']
    rkey = request.session['remote_key']
    if 'ffsession' not in request.session:
        request.session['ffsession'] = friendfeed.FriendFeed(uname, rkey)
    ffsession = request.session['ffsession']
    if 'favs' not in request.session:
        request.session['favs'] = ffsession.fetch_favorites()
    favs = request.session['favs']
    if 'blind_entries' not in request.session:
        request.session['blind_entries'] = []
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
            request.session['blind_entries'].append(btxt)
        # TODO: Don't hardcode 5
        # TODO: Unique by author
        request.session['blind_entries'] = request.session['blind_entries'][:5]

    if entry_index+1 < len(request.session['blind_entries']):
        # TODO: Don't hardcode thisurl, infer it from urls.py or somewhere
        thisurl = "/vote/%d" % (entry_index+1)
    else:
        # TODO: Don't hardcode thisurl, infer it from urls.py or somewhere
        thisurl = "/results/%d" % (entry_index+1)

    return render_to_response("vote.html", {"entry": request.session['blind_entries'][entry_index], "thisurl": thisurl, "percentstr": "%s done" % percent(entry_index, len(request.session['blind_entries'])), "debug": simplejson.dumps(request.session['votes'], indent=4)}, context_instance=RequestContext(request))
#    return render_to_response("vote.html", {"entry": request.session['blind_entries'][entry_index], "thisurl": thisurl, "percentstr": "%s done" % percent(entry_index, len(request.session['blind_entries'])), "debug": simplejson.dumps(request.session['blind_entries'], indent=4)}, context_instance=RequestContext(request))
#    return render_to_response("vote.html", {"blind_entries": [blind_entries[number]]}, context_instance=RequestContext(request))
#    return render_to_response("vote.html", {"blind_entries": blind_entries, "debug": simplejson.dumps(favs, indent=4)}, context_instance=RequestContext(request))

def friendfeed_results(request, entry_index, rating):
    add_vote(request, entry_index, rating)

    results = []
    for i in request.session['votes']:
        # TODO: Gracefully fail instead of assert?
        assert request.session['votes'][i] in [+1, -1, None]
        results.append((i, request.session['votes'][i]))

    return render_to_response("results.html", {"results": results, "debug": request.session['votes']}, context_instance=RequestContext(request))

def percent(a, b):
    """
    Return percentage string of a and b, e.g.:
        "1 of 10 (10%)"
    """
    assert a <= b
    assert a >= 0
    assert b > 0
    return "%s of %s (%.2f%%)" % (a, b, 100.*a/b)
