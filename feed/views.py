from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from random import shuffle
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

def friendfeed_do_vote(request,rating):
    if('post_index' not in request.session):
        request.session['post_index']=-1
        return HttpResponseRedirect("/vote/")
    #todo save the vote
    request.session['post_index']+=1
    return HttpResponseRedirect("/vote/")

def friendfeed_vote(request):
    """
    """
    if('post_index' not in request.session):
        request.session['post_index']=0
    entry_index = request.session['post_index']
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
        shuffle(request.session['blind_entries'])

    request.session['post_index']+= 1
    entry_index+=1
    if entry_index < len(request.session['blind_entries']):
        # TODO: Don't hardcode thisurl, infer it from urls.py or somewhere
        thisurl = "/vote"
    else:
        # TODO: Don't hardcode thisurl, infer it from urls.py or somewhere
        thisurl = "/results/"

    return render_to_response("vote.html", {"entry": request.session['blind_entries'][entry_index], "thisurl": thisurl, "percentstr": "%s done" % percent(entry_index, len(request.session['blind_entries'])), "debug": simplejson.dumps(request.session['blind_entries'], indent=4)}, context_instance=RequestContext(request))
#    return render_to_response("vote.html", {"blind_entries": [blind_entries[number]]}, context_instance=RequestContext(request))
#    return render_to_response("vote.html", {"blind_entries": blind_entries, "debug": simplejson.dumps(favs, indent=4)}, context_instance=RequestContext(request))

def percent(a, b):
    """
    Return percentage string of a and b, e.g.:
        "1 of 10 (10%)"
    """
    assert a <= b
    assert a >= 0
    assert b > 0
    return "%s of %s (%.2f%%)" % (a, b, 100.*a/b)
