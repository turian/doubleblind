from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from urllib2 import HTTPError

from feed.views import friendfeed_initialize_trials
from ffauth.views import logout

def start(request):
    # TODO: Better way of seeing if user is authenticated
    if 'username' in request.session:
        try:
            friendfeed_initialize_trials(request)
        except HTTPError:            
            return logout(request, msg="There was a problem authenticating you. Please try again.")
        return render_to_response("start.html", {"username": request.session["username"]}, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect("/login")
