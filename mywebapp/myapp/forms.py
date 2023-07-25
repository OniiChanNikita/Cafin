from django import forms

class LoginForm(forms.Form):
	username_form = forms.CharField(max_length=255, label='username')
	password_form = forms.CharField(widget=forms.PasswordInput, label='password')
	email_form = forms.CharField(widget=forms.EmailInput, label='email')
