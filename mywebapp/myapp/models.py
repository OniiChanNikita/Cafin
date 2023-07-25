from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class UserProfile(models.Model):
	username = models.OneToOneField(User, on_delete=models.CASCADE)
	password = models.CharField(max_length=50)
	email = models.EmailField(max_length=155)
	slug_indetefication = models.SlugField(unique=True, null=False)

	def get_absolute_url_profile(self):
		return reverse("article_detail", kwargs={"slug_indetefication": self.slug_indetefication}) 