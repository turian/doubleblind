from django import forms

class FFLoginForm(forms.Form):
	username = forms.CharField(max_length=30)
	remote_key = forms.CharField(max_length=30)
