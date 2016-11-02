from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.core import validators

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect

def index(request):
    return render(request, 'userauth/login-signup.html')

def signup(request):
	firstname = request.POST['firstname']
	lastname = request.POST['lastname']
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
	
	if User.objects.filter(email=email).exists():
		return HttpResponse("Email already exists!")

	user = User.objects.create_user(user, email, password)
	user.first_name = firstname
	user.last_name = lastname
	user.save()
	return HttpResponseRedirect(reverse('userauth:index'))

def signin(request):
	email = request.POST['email']
	password =  request.POST['password']
	user1 = User.objects.get(email = email)
	user = authenticate(username = user1.username, password = password)
	if user is not None:
		login(request, user)
		return HttpResponseRedirect(reverse('userauth:index'))
	else:
		return HttpResponse('Email or password did not match')


