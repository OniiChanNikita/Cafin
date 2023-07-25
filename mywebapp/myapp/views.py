from django.shortcuts import render, redirect
from .models import Item
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout, login, authenticate
from .models import *
from .forms import *
import random


def specific_string(length): 
    sample_string = 'pqrstuvwxy' 
    result = ''.join((random.choice(sample_string)) for x in range(length)) 
    return result

def index(request):
	if not request.user.is_authenticated:
		return render(request, 'myapp/index.html', {})
	else: 
		if request.user.is_superuser:
			user_satatus = 'admin'
		else:
			user_satatus = 'user'
		return render(request, 'myapp/home/index.html', {'user_satatus': user_satatus})

def login_user(request):
	if not request.user.is_authenticated:
		if request.method == 'POST':
			print('aa')
			login_form = LoginForm(request.POST)
			if login_form.is_valid():
				username = request.POST['username_form']
				password = request.POST['password_form']
				email = request.POST['email_form']
				user = User.objects.create_user(username = username, password = password, email = email)
				user.save()

				user_auth = authenticate(request, username=username, password=password)
				if user is not None:
					UserProfile.objects.create(username = User.objects.get(username = username), password = password, email = email, slug_indetefication = specific_string(10))
					login(request, user_auth)
					return redirect('index')
		else:
			login_form = LoginForm()
		return render(request, 'myapp/login.html', {'login_form': login_form})
	else:
		return render(request, 'myapp/main.html')

@login_required
def logout_user(request):
	logout(request)
	return redirect('index')

@login_required
def main_profile(request):
	return render(request, 'myapp/main/src/index.html', {})