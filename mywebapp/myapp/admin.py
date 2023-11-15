from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(FinanceSettlement)
admin.site.register(OperatingExpens)
admin.site.register(MessageChat)
admin.site.register(MessagerModel)