from django.contrib import admin
from .models import Users, AccountTiers, OriginalImages, ResizeImages

admin.site.register(AccountTiers)
admin.site.register(Users)
admin.site.register(OriginalImages)
admin.site.register(ResizeImages)

