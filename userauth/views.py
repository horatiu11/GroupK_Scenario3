from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.core import validators

from django.contrib.auth.models import User

def index(request):
    return render(request, 'userauth/index.html')

def login(request):
	user = request.POST['user']
	email = request.POST['email']
	password = request.POST['password']
	repassword = request.POST['repassword']
	
	if not(user and email and password and repassword):
		return HttpResponse('Complete all fields!')
	
	if password != repassword:
		return HttpResponse('Passwords do not match')
	
	if len(password) < 6:
		return HttpResponse('Passwords must be at least 6 characters long')
	
	try:
		validators.validate_email(email)
	except:
		return HttpResponse('Email is not valid!')
	
	user = User.objects.create_user(user)
	user.email = email
	user.password = password
	user.save()
	return HttpResponseRedirect(reverse('userauth:index'))