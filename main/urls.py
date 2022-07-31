from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from . import views

router = routers.DefaultRouter(trailing_slash=False)
router.register('users', views.UsersView, 'users')
router.register('account_tiers', views.AccountTiersView, 'account_tiers')
router.register('image_upload', views.ImageUpload, 'image_upload')
router.register('expires_images', views.ExpiresImages, 'expires_images')

urlpatterns = [
    path('', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
