from django.contrib import admin
from .models import Users, AccountTiers, Images

admin.site.register(AccountTiers)
admin.site.register(Users)
admin.site.register(Images)
