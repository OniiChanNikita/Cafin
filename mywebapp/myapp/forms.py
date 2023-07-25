from django import forms

class RegisterForm(forms.Form):
	username_form = forms.CharField(max_length=255, label='username')
	password_form = forms.CharField(widget=forms.PasswordInput, label='password')
	confirm_password_form = forms.CharField(widget=forms.PasswordInput, label='confirm_password')
	email_form = forms.CharField(widget=forms.EmailInput, label='email')

	def clean(self):
		cleaned_data = super().clean()
		password = cleaned_data.get("password_form")
		confirm_password = cleaned_data.get("confirm_password_form")

		if password and confirm_password and password != confirm_password:
			raise forms.ValidationError("Пароли не совпадают. Пожалуйста, введите одинаковые пароли.")

class LoginForm(forms.Form):
	username_form = forms.CharField(max_length=255, label='username')
	password_form = forms.CharField(widget=forms.PasswordInput, label='password')


class ProfileEditForm(forms.Form):
	username_form = forms.CharField(max_length=255, label='username', required = False)
	email_form = forms.EmailField(max_length=155, required = False, label='email')
	first_name_form = forms.CharField(max_length=255, required = False, label='first_name')
	last_name_form = forms.CharField(max_length=255, required = False, label='last_name')
	address_form = forms.CharField(widget = forms.Textarea, required = False, label='address')
	city_form = forms.CharField(max_length=255, required = False, label='city')
	country_form = forms.CharField(max_length=255, required = False, label='country')
	postal_code_form = forms.IntegerField(required = False, label='postal_code')
	about_me_form = forms.CharField(widget = forms.Textarea, required = False, label='about_me')


class FormCreateSettlement(forms.Form):
	financial_identity_name_form = forms.CharField(max_length=500, label='financial_identity_name')
	net_profit_form = forms.IntegerField(label = 'net_profit')
	total_attachment_form = forms.IntegerField(label = 'total_attachment')
	operating_expens_form = forms.IntegerField(label = 'operating_expens')
	name_operating_expense_form = forms.CharField(max_length=500, label = 'name_operating_expense')
	