from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

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

class FriendsUser(models.Model):
	user_request = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'user_request')
	user_receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'user_receiver')
	access = models.CharField(max_length=50, null=True)
	def __str__(self):
		return self.user_request.username+' '+self.user_receiver.username

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
	slug_financesettlement = models.SlugField(unique=True, null=True)
	is_completed = models.CharField(null=True, max_length=5);

	def make_complete(self):
		self.is_completed = 'True'

	def make_not_comlete(self):
		self.is_completed = 'False'

	def get_absolute_url_profile(self):
		return reverse("open_finance_settlement", kwargs={"slug_financesettlement": self.slug_financesettlement}) 

	def __str__(self):
		return self.username.username

class MessagerModel(models.Model):
	username = models.ForeignKey(User, on_delete=models.CASCADE)
	message = models.TextField(null=True)
	created_at = models.DateTimeField(default=timezone.now)
	is_read = models.BooleanField(default=False)

	def __str__(self):
		return self.username.username

# class MessageRecipient(models.Model):
# 	username = models.ForeignKey(User, on_delete=models.CASCADE)
# 	message = models.TextField(null = True)
# 	created_at = models.DateTimeField(default=timezone.now)

class MessageChat(models.Model):
	user1_search = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1_chats')
	user2_search = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2_chats')
	user = models.ManyToManyField(MessagerModel)
	slug_num = models.CharField(max_length=15, unique=True)
	last_message = models.ForeignKey(MessagerModel, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
	is_read_num_user1 = models.IntegerField(default=0)
	is_read_num_user2 = models.IntegerField(default=0)


	def __str__(self):
		return self.slug_num

	def get_absolute_url(self):
		return reverse("chat_detail", args=[str(self.slug_num)])


@receiver(m2m_changed, sender=MessageChat.user.through)
def update_last_message(sender, instance, action, reverse, model, pk_set, **kwargs):
	if action == 'post_add':
		if pk_set:
			last_message_id = max(pk_set)
			instance.last_message_id = last_message_id
			instance.save()
	instance.is_read_num_user1 = instance.user.filter(username=instance.user1_search, is_read=False).count()
	instance.is_read_num_user2 = instance.user.filter(username=instance.user2_search, is_read=False).count()
	instance.save()

