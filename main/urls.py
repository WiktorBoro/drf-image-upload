from django.urls import include, path, re_path
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from . import views

router = routers.DefaultRouter(trailing_slash=False)
router.register('users', views.UserImageView, basename='users image list')
router.register('account-tiers', views.AccountTiersView, basename='account tiers')
router.register('image-upload', views.ImageUpload, basename='image upload')
router.register('expires-image', views.ExpiresImages, basename='expires image')

urlpatterns = [
    path('', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
