from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

def start(request):
    # TODO: Better way of seeing if user is authenticated
    if 'username' in request.session:
        return render_to_response("start.html", {"username": request.session["username"]}, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect("/login")
