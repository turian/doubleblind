# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from doubleblind.ffauth.forms import FFLoginForm
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
			return HttpResponseRedirect("/vote")
		else:
			return HttpResponse("did not validate")
	else:
		form = FFLoginForm()
	logged_in = (('username' in request.session) and ('remote_key' in request.session))
	return render_to_response("fflogin.html",{'form':form,'logged_in':logged_in})
	
def logout(request):
    for k in ["username", "remote_key", "ff_auth", "blind_entries", "ffsession", "favs"]:
		del request.session[k]
	return render_to_response("fflogout.html",{})
