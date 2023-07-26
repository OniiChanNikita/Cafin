from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
	username = models.OneToOneField(User, on_delete=models.CASCADE)
	password = models.CharField(max_length=50)
	email = models.EmailField(max_length=155)
	first_name = models.CharField(max_length=255, null=True)
	last_name = models.CharField(max_length=255, null=True)
	address = models.TextField(null=True)
	city = models.CharField(max_length=255, null=True)
	country = models.CharField(max_length=255, null=True)
	postal_code = models.IntegerField(null=True)
	about_me = models.TextField(null=True)
	slug_indetefication = models.SlugField(unique=True, null=False)
	created_at = models.DateTimeField(default=timezone.now)

	def get_absolute_url_profile(self):
		return reverse("article_detail", kwargs={"slug_indetefication": self.slug_indetefication}) 

	def __str__(self):
		return self.username.username




class OperatingExpens(models.Model):
	username = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
	name_operating_expense = models.CharField(max_length=500)
	operating_expens = models.IntegerField()
	created_at = models.DateTimeField(default=timezone.now)
	def __str__(self):
		return self.name_operating_expense



class FinanceSettlement(models.Model):
	username = models.ForeignKey(User, on_delete=models.CASCADE)
	financial_identity_name = models.CharField(max_length=500)
	net_profit = models.IntegerField()
	total_attachment = models.IntegerField()
	percent_net_profit = models.IntegerField()
	input_values = models.ManyToManyField(OperatingExpens)
	created_at = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.username.username
