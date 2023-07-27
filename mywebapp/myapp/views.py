from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout, login, authenticate
from .models import *
from django.db.models import *
from django.db.models.functions import ExtractMonth
from .forms import *
from django.forms.formsets import formset_factory
import random
from django.forms import modelformset_factory
from django.utils import timezone


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
			financesettlement = FinanceSettlement.objects.all()
		else:
			admin_status = False
			financesettlement = FinanceSettlement.objects.filter(username = request.user)

		total_sales=financesettlement.count()
		all_percent = financesettlement.aggregate(all_percent=Avg('percent_net_profit'))['all_percent']
		print(all_percent)

		net_profit_by_month = []
		procent_net_profit_by_month = []

		for month in range(1, 13):
			settlement = financesettlement.filter(created_at__month=month)
			net_progit_sum = settlement.aggregate(net_progit_sum=Sum('net_profit'))['net_progit_sum']
			net_profit_by_month.append(net_progit_sum)
		for month in range(1, 13):
			settlement = financesettlement.filter(created_at__month=month)
			all_percent_settlement = settlement.aggregate(all_percent_settlement=Avg('percent_net_profit'))['all_percent_settlement']
			procent_net_profit_by_month.append(all_percent_settlement)

		current_datetime = timezone.now()
		if financesettlement.filter(created_at__month=current_datetime.month).count() >= financesettlement.filter(created_at__month=current_datetime.month-1).count() and financesettlement.filter(created_at__month=current_datetime.month).count() != 0:
			procent_since_last_month_sales = (1-(financesettlement.filter(created_at__month=current_datetime.month-1).count() / financesettlement.filter(created_at__month=current_datetime.month).count()))*100
		else: 
			procent_since_last_month_sales = -(financesettlement.filter(created_at__month=current_datetime.month).count() / financesettlement.filter(created_at__month=current_datetime.month-1).count())*100

		if financesettlement.filter(created_at__month=current_datetime.month).aggregate(all_percent=Avg('percent_net_profit'))['all_percent'] >= financesettlement.filter(created_at__month=current_datetime.month-1).aggregate(all_percent=Avg('percent_net_profit'))['all_percent'] and financesettlement.filter(created_at__month=current_datetime.month).aggregate(all_percent=Avg('percent_net_profit'))['all_percent'] != 0:
			procent_since_last_month_net = (1-(financesettlement.filter(created_at__month=current_datetime.month-1).aggregate(all_percent=Avg('percent_net_profit'))['all_percent'] / financesettlement.filter(created_at__month=current_datetime.month).aggregate(all_percent=Avg('percent_net_profit'))['all_percent']))*100
		else: 
			procent_since_last_month_net = -(financesettlement.filter(created_at__month=current_datetime.month).aggregate(all_percent=Avg('percent_net_profit'))['all_percent'] / financesettlement.filter(created_at__month=current_datetime.month-1).aggregate(all_percent=Avg('percent_net_profit'))['all_percent'])*100


		return render(request, 'myapp/home/index.html', {'admin_status': admin_status, 'total_sales':total_sales, 'all_percent': round(all_percent, 2),
	 													'net_profit_by_month':net_profit_by_month, 'procent_net_profit_by_month': procent_net_profit_by_month,
	 													'procent_since_last_month_sales': round(procent_since_last_month_sales, 2), 'procent_since_last_month_net': round(procent_since_last_month_net, 2)})

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
			not_net_profit = 0
			user = User.objects.get(username=request.user.username)

			financial_identity_name = request.POST['financial_identity_name_form']
			net_profit = request.POST['net_profit_form']
			total_attachment = request.POST['total_attachment_form']

			for f_form in formset:
				if f_form.is_valid() and f_form.has_changed():
					f_form.username = user
					f_form.save()
					print(f_form.cleaned_data['operating_expens'])
					operating_expense = OperatingExpens.objects.filter(operating_expens = f_form.cleaned_data['operating_expens'],
																		name_operating_expense =  f_form.cleaned_data['name_operating_expense']).first()
					if operating_expense:
						operating_expense.username = request.user
						operating_expense.save()
					not_net_profit+=f_form.cleaned_data['operating_expens']
					querty_list.append(operating_expense)
			percent_net_profit = -(int(net_profit)/int(not_net_profit))*100
			if int(not_net_profit)<int(net_profit):
				percent_net_profit = (1-(int(not_net_profit)/int(net_profit)))*100
			finance_settlement = FinanceSettlement.objects.create(
				username=user,
				financial_identity_name=financial_identity_name,  
				net_profit=net_profit,  
				total_attachment=total_attachment,
				percent_net_profit=percent_net_profit,
				slug_financesettlement=specific_string(10),
			)
			finance_settlement.input_values.add(*querty_list)
			
	else:
		form = FormCreateSettlement()
		formset = InfiniteInputFormSet(queryset=OperatingExpens.objects.none())
	return render(request, 'myapp/home/create_finance_settlement.html',  {'form': form, 'formset': formset})

@login_required
def finance_tables(request):
	financesettlement = FinanceSettlement.objects.filter(username = request.user)
	return render(request, 'myapp/home/tables.html', {"financesettlement": financesettlement})

@login_required
def open_finance_settlement(request, slug_financesettlement):
	get_object_slug_financesettlement = get_object_or_404(FinanceSettlement, slug_financesettlement=slug_financesettlement)
	get_obj = get_object_slug_financesettlement.input_values.all()
	get_obj_avg = get_obj.aggregate(get_obj_avg=Avg('operating_expens'))['get_obj_avg']
	get_obj_avg_total = get_object_slug_financesettlement.total_attachment
	get_obj_avg_net = get_object_slug_financesettlement.net_profit
	if get_obj_avg_total > get_obj_avg_net:
		get_obj_avg_tn = -(get_obj_avg_net/get_obj_avg_total)*100
	else:
		get_obj_avg_tn = (1-(get_obj_avg_total/get_obj_avg_net))*100
	return render(request, 'myapp/home/open_tables.html', {'get_obj': get_object_slug_financesettlement, 'get_expenses_obj': get_object_slug_financesettlement.input_values.all(),
															 'get_obj_count': get_object_slug_financesettlement.input_values.all().count(), 'get_obj_avg': round(get_obj_avg, 2),
															 'get_obj_avg_total_net': round(get_obj_avg_tn, 2)})
@login_required
def delete_operating(request, element_id):
	if request.method == 'DELETE':
		element = get_object_or_404(OperatingExpens, id=element_id)
		element_perent = FinanceSettlement.objects.filter(username = request.user, input_values = element)

		if element_perent.first().input_values.count()>1:
			slug_before_deletion = element_perent.slug_financesettlement
			element.delete()
			return redirect('open_finance_settlement', slug=slug_before_deletion)
	return redirect('index')