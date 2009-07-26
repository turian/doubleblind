# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from doubleblind.ffauth.forms import FFLoginForm
from doubleblind.feed.models import Rater
def login(request):
	if request.method=='POST':
		#user is authenticated if form validates
		form = FFLoginForm(request.POST)
		if(form.is_valid()):
			#login logic here
			#fields accessed via form.cleaned_data[fieldname]
			request.session['username'] = form.cleaned_data['username']
			request.session['remote_key'] = form.cleaned_data['remote_key']
			request.session['ff_auth'] = True
			rater,created = Rater.objects.get_or_create(name=form.cleaned_data['username'])
			rater.remote_key=form.cleaned_data['remote_key']
			rater.save()
			return HttpResponseRedirect("/start")
		else:
			return HttpResponse("did not validate")
	else:
		form = FFLoginForm()
	logged_in = (('username' in request.session) and ('remote_key' in request.session))
	return render_to_response("fflogin.html",{'form':form,'logged_in':logged_in})
	
def logout(request, msg="You are now logged out."):
    #for k in ["username", "remote_key", "ff_auth", "blind_entries", "ffsession", "favs"]:
    for k in request.session.keys():
		del request.session[k]
    return render_to_response("fflogout.html",{"msg": msg})
