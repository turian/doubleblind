from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from doubleblind.feed.models import Post,Rating,Poster,Rater
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

rating_score = {'thumbsup':+1,'thumbsdown':-1,'pass':0}
def add_vote(request, entry_index, rating):
    """
    TODO: This shouldn't be in views
    """
    favs = request.session['favs']
    postData = favs[entry_index]
    userData = postData['from']
    rater,created = Rater.objects.get_or_create(host=request.META['REMOTE_ADDR'])
    if created:
       rater.save()
    poster,created = Poster.objects.get_or_create(name=userData['id'],text=simplejson.dumps(userData))
    if created:
        poster.save()
    post = Post(poster=poster,post_id=postData['id'],text=simplejson.dumps(postData))
    post.save()
    rating = Rating(post=post,rater=rater,score=rating_score[rating])
    rating.save()

def friendfeed_do_vote(request, rating):
    add_vote(request,request.session['entry_index'], rating)
    request.session['entry_index']+=1
    return HttpResponseRedirect("/vote/")

def friendfeed_vote(request, rating=None):
    """
    """
    if 'entry_index' not in request.session:
        request.session['entry_index'] = 0
    entry_index = request.session['entry_index']
    # TODO: Store previous rating
    if 'votes' not in request.session:
        request.session['votes']  = {}

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
        favs = ffsession.fetch_favorites()['entries']
        request.session['favs'] = []
        users = {}
        # Find 5 posts by unique people
        for f in favs:
            # TODO: Don't hardcode 5
            if len(request.session['favs']) >= 5: break
            u = f["from"]["id"]
            # Unique posts by author
            if u in users: continue
            request.session['favs'].append(f)
            users[u] = True

    favs = request.session['favs']
    if 'blind_entries' not in request.session:
        request.session['blind_entries'] = []
        for e in favs:
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

    if entry_index+1 < len(request.session['blind_entries']):
        # TODO: Don't hardcode thisurl, infer it from urls.py or somewhere
        thisurl = "/vote"
    else:
        # TODO: Don't hardcode thisurl, infer it from urls.py or somewhere
        thisurl = "/results/%d" % (entry_index+1)

    return render_to_response("vote.html", {"entry": request.session['blind_entries'][entry_index], "thisurl": thisurl, "percentstr": "%s done" % percent(entry_index, len(request.session['blind_entries'])), "debug": favs}, context_instance=RequestContext(request))
#    return render_to_response("vote.html", {"entry": request.session['blind_entries'][entry_index], "thisurl": thisurl, "percentstr": "%s done" % percent(entry_index, len(request.session['blind_entries'])), "debug": simplejson.dumps(request.session['blind_entries'], indent=4)}, context_instance=RequestContext(request))
#    return render_to_response("vote.html", {"blind_entries": [blind_entries[number]]}, context_instance=RequestContext(request))
#    return render_to_response("vote.html", {"blind_entries": blind_entries, "debug": simplejson.dumps(favs, indent=4)}, context_instance=RequestContext(request))

def friendfeed_results(request, entry_index, rating):
    add_vote(request, entry_index, rating)

    results = []
    for i in request.session['votes']:
        # TODO: Gracefully fail instead of assert?
        assert request.session['votes'][i] in [+1, -1, None]
#        user = friendfeed.fetch_user_profile(request.session['blind_entries']
#        request.session['favs'] = ffsession.fetch_favorites()
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
