from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.core import validators

from django.utils import timezone

from django.contrib.auth.models import User
from mainapp.models import Reference, ReferenceList
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

def index(request):
	if 'regist' in request.session:
		del request.session['regist']

	if request.user.is_authenticated:
		return HttpResponseRedirect(reverse('mainapp:mainpage'))
	return render(request, 'mainapp/index.html')

def authentication(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect(reverse('mainapp:mainpage'))
	return render(request, 'mainapp/login-signup.html')

def mainpage(request):
	if 'regist' in request.session:
		del request.session['regist']

	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('mainapp:authentication'))
	try:
		reflist = ReferenceList.objects.all().filter(owner = request.user)
	except ReferenceList.DoesNotExist:
		reflist = None

	context = {'referencesLists' : reflist}
	return render(request, 'mainapp/mainpage.html', context)

def signout(request):
	if 'regist' in request.session:
		del request.session['regist']

	logout(request)
	return HttpResponseRedirect(reverse('mainapp:index'))

def signup(request):
	if 'regist' in request.session:
		del request.session['regist']

	if request.user.is_authenticated:
		return HttpResponseRedirect(reverse('mainapp:mainpage'))
	firstname = request.POST['firstname']
	lastname = request.POST['lastname']
	user = request.POST['user']
	email = request.POST['email']
	password = request.POST['password']
	repassword = request.POST['repassword']
	
	if not(user and email and password and repassword and firstname and lastname):
		request.session['errormessage'] = 'Please complete all field in registration form!'
		return HttpResponseRedirect(reverse('mainapp:errormsg'))
	
	if password != repassword:
		request.session['errormessage'] = 'The passwords inserted do not match!'
		return HttpResponseRedirect(reverse('mainapp:errormsg'))

	if len(password) < 6:
		request.session['errormessage'] = 'Passwords must be at least 6 characters long!'
		return HttpResponseRedirect(reverse('mainapp:errormsg'))
	
	try:
		validators.validate_email(email)
	except:
		request.session['errormessage'] = 'Email is not valid!'
		return HttpResponseRedirect(reverse('mainapp:errormsg'))
	
	if User.objects.filter(email=email).exists():
		request.session['errormessage'] = 'Email already used!'
		return HttpResponseRedirect(reverse('mainapp:errormsg'))

	user = User.objects.create_user(user, email, password)
	user.first_name = firstname
	user.last_name = lastname
	user.save()
	request.session['regist'] = 'YES'
	return HttpResponseRedirect(reverse('mainapp:authentication'))

def signin(request):
	if 'regist' in request.session:
		del request.session['regist']

	if request.user.is_authenticated:
		return HttpResponseRedirect(reverse('mainapp:mainpage'))
	email = request.POST['email']
	password =  request.POST['password']

	try:
		user1 = User.objects.get(email = email)
	except User.DoesNotExist:
		request.session['errormessage'] = 'Credentials are wrong!'
		return HttpResponseRedirect(reverse('mainapp:errormsg'))
	
	user1 = User.objects.get(email = email)

	user = authenticate(username = user1.username, password = password)
	if user is not None:
		login(request, user)
		return HttpResponseRedirect(reverse('mainapp:index'))
	else:
		request.session['errormessage'] = 'Credentials are wrong!'
		return HttpResponseRedirect(reverse('mainapp:errormsg'))

def addref(request):
	if 'regist' in request.session:
		del request.session['regist']

	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('mainapp:authentication'))
	
	title = request.POST['title']
	if title is '':
		request.session['errormessage'] = 'A title is required!'
		return HttpResponseRedirect(reverse('mainapp:errormsg'))

	author =  request.POST['author']
	link =  request.POST['urlink']
	source =  request.POST['source']
	notes = request.POST['notes']

	selectedList = int(request.POST.get('selectedList', -1))
	if selectedList is -1:
		request.session['errormessage'] = 'You should choose a list to add the reference in!'
		return HttpResponseRedirect(reverse('mainapp:errormsg'))

	u = request.user

	if selectedList is 0:
		listname = request.POST['listname']
		reflist = ReferenceList(owner = u, name = listname, createdAt = timezone.now())
		reflist.save()
	else:
		reflist = ReferenceList.objects.get(id = selectedList)

	ref = Reference(reference_list = reflist, title = title, author = author, website = link, source = source, notes = notes)
	ref.save()

	return HttpResponseRedirect(reverse('mainapp:mainpage'))

def deleteref(request):
	if 'regist' in request.session:
		del request.session['regist']

	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('mainapp:authentication'))
	ID = request.POST['id']
	Reference.objects.filter(id = ID).delete()

	return HttpResponseRedirect(reverse('mainapp:mainpage'))

def deletelist(request):
	if 'regist' in request.session:
		del request.session['regist']

	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('mainapp:authentication'))
	ID = request.POST['id']
	ReferenceList.objects.filter(id = ID).delete()

	return HttpResponseRedirect(reverse('mainapp:mainpage'))

def saveref(request):
	if 'regist' in request.session:
		del request.session['regist']

	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('mainapp:authentication'))
	title = request.POST['title']
	if title is '':
		request.session['errormessage'] = 'A title is required!'
		return HttpResponseRedirect(reverse('mainapp:errormsg'))

	author =  request.POST['author']
	link =  request.POST['urlink']
	source =  request.POST['source']
	notes = request.POST['notes']
	ID = request.POST['id']

	ref = Reference.objects.get(id = ID)
	ref.title = title
	ref.author = author
	ref.website = link
	ref.source = source
	ref.notes = notes
	ref.save()

	return HttpResponseRedirect(reverse('mainapp:mainpage'))

def errormsg(request):
	if 'regist' in request.session:
		del request.session['regist']

	errormessage = request.session['errormessage']
	request.session['errormessage'] = None
	
	context = {'errormessage' : errormessage}
	return render(request, 'mainapp/errormessage.html', context)