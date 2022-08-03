from django.contrib import admin
from .models import Users, AccountTiers, OriginalImages, ResizeImages


class AccountTiersAdmin(admin.ModelAdmin):
    class UserAccountTiersAdmin(admin.TabularInline):
        model = Users
        fields = ['user_name']
        max_num = 0

    list_display = ['account_tier_name',
                    'link_to_the_originally_uploaded_file',
                    'ability_to_generate_expiring_links']
    inlines = [UserAccountTiersAdmin]


@admin.action(description='Delete images with file')
def delete_images_with_file(modeladmin, request, images):
    for img in images:
        img.image.delete(save=True)
        img.delete()


class ResizeImageLinksAdmin(admin.TabularInline):
    model = ResizeImages
    fields = ['resize_image', 'height', 'width', 'expiring_time']
    max_num = 0


class OriginalImagesAdmin(admin.ModelAdmin):
    @admin.display(ordering='user__user_name', description='User name')
    def get_user_name(self, obj):
        return obj.user.user_name

    list_display = ['image_name', 'width', 'height', 'get_user_name']

    actions = [delete_images_with_file]
    inlines = [ResizeImageLinksAdmin]


class OrginialImageLinksAdmin(admin.TabularInline):
    model = OriginalImages
    fields = ['image_name', 'height', 'width', 'image']
    max_num = 0


class UserAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'account_tier']
    inlines = [OrginialImageLinksAdmin]


admin.site.register(AccountTiers, AccountTiersAdmin)
admin.site.register(Users, UserAdmin)
admin.site.register(OriginalImages, OriginalImagesAdmin)
admin.site.register(ResizeImages)

