from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout, login, authenticate
from .models import *
from django.db.models import *
from django.db.models.functions import ExtractMonth
from .forms import *
from django.forms.formsets import formset_factory
from django.forms import modelformset_factory
from django.utils import timezone
import random

def page_not_found_view(request, exception):
	return render(request, 'myapp/home/page-404.html', status=404)

def permission_denied_view(request, exception):
	return render(request, 'myapp/home/page-403.html', status=403)

def server_error_view(request):
	return render(request, 'myapp/home/page-500.html', status=500)

def specific_string(length): 
    sample_string = 'pqrstuvwxy' 
    result = ''.join((random.choice(sample_string)) for x in range(length)) 
    return result

def generate_random_number():
    random_number = random.randrange(10**14, 10**15)
    return random_number



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
		if all_percent == None:
			all_percent = 0

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
		if total_sales > 1:
			if financesettlement.filter(created_at__month=current_datetime.month).count() >= financesettlement.filter(created_at__month=current_datetime.month-1).count() and financesettlement.filter(created_at__month=current_datetime.month).count() != 0 and financesettlement.filter(created_at__month=current_datetime.month-1).count() != 0:
				procent_since_last_month_sales = (1-(financesettlement.filter(created_at__month=current_datetime.month-1).count() / financesettlement.filter(created_at__month=current_datetime.month).count()))*100
				procent_since_last_month_sales = round(procent_since_last_month_sales, 2)
			else: 
				procent_since_last_month_sales = -(financesettlement.filter(created_at__month=current_datetime.month).count() / financesettlement.filter(created_at__month=current_datetime.month-1).count()*100)
				procent_since_last_month_sales = round(procent_since_last_month_sales, 2)


			if financesettlement.filter(created_at__month=current_datetime.month).aggregate(all_percent=Avg('percent_net_profit'))['all_percent'] >= financesettlement.filter(created_at__month=current_datetime.month-1).aggregate(all_percent=Avg('percent_net_profit'))['all_percent'] and financesettlement.filter(created_at__month=current_datetime.month).aggregate(all_percent=Avg('percent_net_profit'))['all_percent'] != 0 and financesettlement.filter(created_at__month=current_datetime.month-1).aggregate(all_percent=Avg('percent_net_profit'))['all_percent'] != 0:
				procent_since_last_month_net = (1-(financesettlement.filter(created_at__month=current_datetime.month-1).aggregate(all_percent=Avg('percent_net_profit'))['all_percent'] / financesettlement.filter(created_at__month=current_datetime.month).aggregate(all_percent=Avg('percent_net_profit'))['all_percent']))*100
				procent_since_last_month_net = round(procent_since_last_month_net, 2)
			else: 
				procent_since_last_month_net = -(financesettlement.filter(created_at__month=current_datetime.month).aggregate(all_percent=Avg('percent_net_profit'))['all_percent'] / financesettlement.filter(created_at__month=current_datetime.month-1).aggregate(all_percent=Avg('percent_net_profit'))['all_percent'])*100
				procent_since_last_month_net = round(procent_since_last_month_net, 2)

		else:
			procent_since_last_month_sales = 0
			procent_since_last_month_net = 0
		users = MessageChat.objects.filter(Q(user1_search = User.objects.get(username = request.user.username), is_read_num_user2__gt=0) | Q(user2_search = User.objects.get(username = request.user.username), is_read_num_user1__gt=0))
		return render(request, 'myapp/home/index.html', {'friend_notice': FriendsUser.objects.filter(access='unconfirm', user_receiver = request.user),'admin_status': admin_status, 'total_sales':total_sales, 'all_percent': round(all_percent, 2),
	 													'net_profit_by_month':net_profit_by_month, 'procent_net_profit_by_month': procent_net_profit_by_month,
	 													'procent_since_last_month_sales': procent_since_last_month_sales, 'procent_since_last_month_net': procent_since_last_month_net,
	 													"message_notice": MessageChat.objects.filter(Q(user1_search = User.objects.get(username = request.user.username), is_read_num_user2__gt=0) | Q(user2_search = User.objects.get(username = request.user.username), is_read_num_user1__gt=0))})
@login_required
def profile_users(request, slug_username):
	user_obj = get_object_or_404(User, username=slug_username)
	financesettlement = FinanceSettlement.objects.filter(username = user_obj)
	friends = FriendsUser.objects.filter(Q(user_request=request.user, user_receiver=user_obj) | Q(user_request=user_obj, user_receiver=request.user)).first()
	if friends == None:
		label = 'create'
	else:
		label = 'delete'
		if friends.access == 'unconfirm' and friends.user_receiver==request.user:
			label = 'access'
	if request.method == 'POST':
		form_id = request.POST['form_id']
		if form_id == 'form_friend':
			if user_obj.username != request.user.username:
				if label == 'create':
					FriendsUser.objects.create(user_request = request.user, user_receiver=user_obj, access = 'unconfirm')
				elif label == 'access':
					print(friends, friends.access)
					if friends.user_receiver == request.user:
						friends.access = 'confirm'
						friends.save()
				elif label == 'delete':
					FriendsUser.objects.filter(Q(user_request=request.user, user_receiver=user_obj) | Q(user_request=user_obj, user_receiver=request.user)).delete()
	return render(request, 'myapp/home/profile.html', {'user_obj': UserProfile.objects.get(username = user_obj), 'financesettlement': financesettlement, 'label': label,
														 'count_friends': FriendsUser.objects.filter(Q(user_request=request.user, user_receiver=user_obj) | Q(user_request=user_obj, user_receiver=request.user)).count(),
														 'count_projects': financesettlement.count(), 'about_me': UserProfile.objects.get(username=user_obj).about_me})

@login_required
def search_users(request):
	users_obj = []
	if request.method == 'POST':
		search_user = SearchUserForm(request.POST)
		if search_user.is_valid():
			print('hi')
			username = request.POST['username_search_form']
			list_username = []
			for i in User.objects.all():
				if username in i.username:
					list_username.append(i.username)
			print(list_username)

			users_obj = User.objects.filter(username__in = list_username)

	else:
		search_user = SearchUserForm()
	return render(request, 'myapp/home/find_user.html', {'friend_notice': FriendsUser.objects.filter(access='unconfirm', user_receiver = request.user), 'users': users_obj, 'search_user': search_user})

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
		return render(request, 'myapp/main.html', {})

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
		return render(request, 'myapp/main.html', {})

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
			return render(request, 'myapp/home/profile.html', {'friend_notice': FriendsUser.objects.filter(access='unconfirm', user_receiver = request.user),'about_me': UserProfile.objects.get(username=request.user).about_me, 'edit_form': edit_form, 'user_profile': user_profile,
				"message_notice": MessageChat.objects.filter(Q(user1_search = User.objects.get(username = request.user.username), is_read_num_user2__gt=0) | Q(user2_search = User.objects.get(username = request.user.username), is_read_num_user1__gt=0))})
	else:
		edit_form=ProfileEditForm()
	return render(request, 'myapp/home/profile.html', {'friend_notice': FriendsUser.objects.filter(access='unconfirm', user_receiver = request.user),'about_me': UserProfile.objects.get(username=request.user).about_me, 'edit_form': edit_form, 'user_profile': user_profile,
	"message_notice": MessageChat.objects.filter(Q(user1_search = User.objects.get(username = request.user.username), is_read_num_user2__gt=0) | Q(user2_search = User.objects.get(username = request.user.username), is_read_num_user1__gt=0))})

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
	return render(request, 'myapp/home/create_finance_settlement.html',  {'friend_notice': FriendsUser.objects.filter(access='unconfirm', user_receiver = request.user),'form': form, 'formset': formset,
		"message_notice": MessageChat.objects.filter(Q(user1_search = User.objects.get(username = request.user.username), is_read_num_user2__gt=0) | Q(user2_search = User.objects.get(username = request.user.username), is_read_num_user1__gt=0))})

@login_required
def finance_tables(request):
	financesettlement = FinanceSettlement.objects.filter(username = request.user)
	return render(request, 'myapp/home/tables.html', {'friend_notice': FriendsUser.objects.filter(access='unconfirm', user_receiver = request.user),"financesettlement": financesettlement})

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
	return render(request, 'myapp/home/open_tables.html', {'friend_notice': FriendsUser.objects.filter(access='unconfirm', user_receiver = request.user),'get_obj': get_object_slug_financesettlement, 'get_expenses_obj': get_object_slug_financesettlement.input_values.all(),
															 'get_obj_count': get_object_slug_financesettlement.input_values.all().count(), 'get_obj_avg': round(get_obj_avg, 2),
															 'get_obj_avg_total_net': round(get_obj_avg_tn, 2),
															 "message_notice": MessageChat.objects.filter(Q(user1_search = User.objects.get(username = request.user.username), is_read_num_user2__gt=0) | Q(user2_search = User.objects.get(username = request.user.username), is_read_num_user1__gt=0))})
@login_required
def delete_operating(request, element_id):
	if request.method == 'DELETE':
		print('s')
		element = get_object_or_404(OperatingExpens, id=element_id)
		element_perent = FinanceSettlement.objects.filter(username = request.user, input_values = element)
		if element_perent.first().input_values.count()>1:
			slug_before_deletion = element_perent.first().slug_financesettlement
			element.delete()
			return redirect('open_finance_settlement', slug_financesettlement=slug_before_deletion)
	return redirect('index')


@login_required
def delete_table(request, element_id_table):
	if request.method == 'DELETE':
		element = get_object_or_404(FinanceSettlement, username = request.user, id=element_id_table)
		element_input_values = element.input_values.all()
		if element.username == request.user:
			element_input_values.delete()
			element.delete()
			return redirect('finance_tables')
	return redirect('index')

@login_required
def modify_table(request, slug_financesettlement):
	element = get_object_or_404(FinanceSettlement, slug_financesettlement=slug_financesettlement)
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
			finance_settlement = FinanceSettlement.objects.get(
				slug_financesettlement=element.slug_financesettlement,
			)
			finance_settlement.financial_identity_name = financial_identity_name
			finance_settlement.net_profit = net_profit
			finance_settlement.total_attachment = total_attachment
			finance_settlement.percent_net_profit = percent_net_profit
			finance_settlement.input_values.add(*querty_list)
			finance_settlement.save()
	else:
		form = FormCreateSettlement()
		formset = InfiniteInputFormSet(queryset=OperatingExpens.objects.none())
	return render(request, 'myapp/home/create_finance_settlement.html',  {'friend_notice': FriendsUser.objects.filter(access='unconfirm', user_receiver = request.user),'form': form, 'formset': formset,
		"message_notice": MessageChat.objects.filter(Q(user1_search = User.objects.get(username = request.user.username), is_read_num_user2__gt=0) | Q(user2_search = User.objects.get(username = request.user.username), is_read_num_user1__gt=0)), 'element_modify': element})

@login_required
def list_chat_box(request):
	# users = UserProfile.objects.filter(username = request.user)
	users = MessageChat.objects.filter(Q(user1_search = User.objects.get(username = request.user.username)) | Q(user2_search = User.objects.get(username = request.user.username)))
	return render(request, "myapp/chat/list_chat_box.html", {'friend_notice': FriendsUser.objects.filter(access='unconfirm', user_receiver = request.user),'users': users,
	"message_notice": MessageChat.objects.filter(Q(user1_search = User.objects.get(username = request.user.username), is_read_num_user2__gt=0) | Q(user2_search = User.objects.get(username = request.user.username), is_read_num_user1__gt=0))}) #'form_search': form, 'list_chat': list_chat


def create_chat_or_redirect(request, slug_username):
	user_obj = get_object_or_404(User, username=slug_username)
	message_obj = MessageChat.objects.filter(Q(user1_search = User.objects.get(username = request.user.username), user2_search = User.objects.get(username = user_obj.username)) | Q(user1_search = User.objects.get(username = user_obj.username), user2_search = User.objects.get(username = request.user.username))).first()
	print(message_obj)
	if not message_obj:
		print('ok')
		messager1 = MessagerModel.objects.create(username = User.objects.get(username = request.user.username))
		messager2 = MessagerModel.objects.create(username = user_obj)
		MessagerModel.objects.create(username = request.user)
		message = MessageChat.objects.create(user1_search = User.objects.get(username = request.user), user2_search = User.objects.get(username = user_obj.username),slug_num = generate_random_number())
		message.user.add(messager1) 
		message.user.add(messager2) 
		return redirect('chat_box', slug_num = message.slug_num)
	return redirect('chat_box', slug_num = message_obj.slug_num)

@login_required
def chat_box(request, slug_num):
	get_obj_slug = get_object_or_404(MessageChat, slug_num=slug_num)
	for messages in get_obj_slug.user.filter(username = get_obj_slug.user1_search):
		if messages.username != request.user:
			messages.is_read = True
	if get_obj_slug.user1_search == request.user:
		
		get_obj_slug.is_read_num_user1 = 0

	else:
		get_obj_slug.is_read_num_user2 = 0
	print(get_obj_slug.slug_num)
	message_list = []
	for messages in get_obj_slug.user.all():
		if messages.message is not None:
			message_list.append({messages.username: messages.message})

	return render(request, "myapp/chat/chat_box.html", {'friend_notice': FriendsUser.objects.filter(access='unconfirm', user_receiver = request.user),'get_obj_slug':get_obj_slug, 'messages': get_obj_slug.user.all(),
		"message_notice": MessageChat.objects.filter(Q(user1_search = User.objects.get(username = request.user.username), is_read_num_user2__gt=0) | Q(user2_search = User.objects.get(username = request.user.username), is_read_num_user1__gt=0))})