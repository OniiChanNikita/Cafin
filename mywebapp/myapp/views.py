from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout, login, authenticate
from .models import *
from .forms import *
from django.forms.formsets import formset_factory
import random
from django.forms import modelformset_factory



def specific_string(length): 
    sample_string = 'pqrstuvwxy' 
    result = ''.join((random.choice(sample_string)) for x in range(length)) 
    return result

def index(request):
	if not request.user.is_authenticated:
		return render(request, 'myapp/index.html')
	else: 
		if request.user.is_superuser:
			admin_status = True
		else:
			admin_status = False
		return render(request, 'myapp/home/index.html', {'admin_status': admin_status})

def register_user(request):
	if not request.user.is_authenticated:
		if request.method == 'POST':
			register_form = RegisterForm(request.POST)
			if register_form.is_valid():
				username = request.POST['username_form']
				password = request.POST['password_form']
				confirm_password = request.POST['confirm_password_form']
				email = request.POST['email_form']

				user = User.objects.create_user(username = username, password = password, email = email)
				user.save()

				user_auth = authenticate(request, username=username, password=password)
				if user_auth is not None:
					UserProfile.objects.create(username = User.objects.get(username = username), password = password, email = email, slug_indetefication = specific_string(10))
					login(request, user_auth)
					return redirect('index')
		else:
			register_form = RegisterForm()
		return render(request, 'myapp/accounts/register.html', {'register_form': register_form})
	else:
		return render(request, 'myapp/main.html')

def login_user(request):
	if not request.user.is_authenticated:
		if request.method == 'POST':
				login_form = LoginForm(request.POST)
				if login_form.is_valid():
					username = request.POST['username_form']
					password = request.POST['password_form']

					user_auth = authenticate(request, username=username, password=password)
					if user_auth is not None:
						login(request, user_auth)
						return redirect('index')
		else:
			login_form = LoginForm()
		return render(request, 'myapp/accounts/login.html', {'login_form': login_form})
	else:	
		return render(request, 'myapp/main.html')

@login_required
def logout_user(request):
	logout(request)
	return redirect('index')

@login_required
def profile(request):
	user_profile = get_object_or_404(UserProfile, username=request.user)
	if request.method == 'POST':
		edit_form = ProfileEditForm(request.POST)
		if edit_form.is_valid():
			username = request.POST['username_form']
			email = request.POST['email_form']
			postal_code = request.POST['postal_code_form']
			user_profile.first_name = request.POST['first_name_form']
			user_profile.last_name = request.POST['last_name_form']
			user_profile.address = request.POST['address_form']
			user_profile.city = request.POST['city_form']
			user_profile.country = request.POST['country_form']
			user_profile.about_me = request.POST['about_me_form']
			

			if username == '' or username == None:
				username = request.user.username
			if email == '' or email == None:
				email = request.user.email
			if postal_code == '' or postal_code == None:
				postal_code = 0
			user_rename = User.objects.get(username = request.user.username)
			user_rename.username = username
			user_rename.save()
			request.user.username = username
			user_profile.username = User.objects.get(username = username)

			user_profile.email = email
			user_profile.postal_code = postal_code

			user_profile.save()
			return render(request, 'myapp/home/profile.html', {'edit_form': edit_form, 'user_profile': user_profile})
	else:
		edit_form=ProfileEditForm()
	return render(request, 'myapp/home/profile.html', {'edit_form': edit_form, 'user_profile': user_profile})

@login_required
def create_finance_settlement(request):
	InfiniteInputFormSet = modelformset_factory(OperatingExpens, extra=1, fields=('name_operating_expense', 'operating_expens'))
	if request.method == 'POST':
		form = FormCreateSettlement(request.POST)
		formset = InfiniteInputFormSet(request.POST)
		print(form.is_valid(), formset.is_valid())
		if form.is_valid() and formset.is_valid():
			querty_list = []
			user = User.objects.get(username=request.user.username)

			financial_identity_name = request.POST['financial_identity_name_form']
			net_profit = request.POST['net_profit_form']
			total_attachment = request.POST['total_attachment_form']

			for f_form in formset:
				if f_form.is_valid() and f_form.has_changed():
					f_form.save()
					print(f_form.cleaned_data['operating_expens'])
					operating_expense = OperatingExpens.objects.filter(operating_expens = f_form.cleaned_data['operating_expens'],
																		name_operating_expense =  f_form.cleaned_data['name_operating_expense']).first()
					operating_expense.username = user
					querty_list.append(operating_expense)
			print(querty_list, '<-------------------')

			finance_settlement = FinanceSettlement.objects.create(
				username=user,
				financial_identity_name=financial_identity_name,  # Здесь вы можете указать имя финансовой свертки, если необходимо
				net_profit=net_profit,  # Здесь вы можете указать начальное значение чистой прибыли, если необходимо
				total_attachment=total_attachment  # Здесь вы можете указать начальное значение общего вложения, если необходимо
			)
			finance_settlement.input_values.add(*querty_list)
			
	else:
		form = FormCreateSettlement()
		formset = InfiniteInputFormSet(queryset=OperatingExpens.objects.none())
	return render(request, 'myapp/home/create_finance_settlement.html',  {'form': form, 'formset': formset})
