from rest_framework import viewsets
from .serializers import UsersSerializer, AccountTiersSerializer, ImagesSerializer
from .models import Users, AccountTiers, Images


class UsersView(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    http_method_names = ['get', 'post']


class AccountTiersView(viewsets.ModelViewSet):
    queryset = AccountTiers.objects.all()
    serializer_class = AccountTiersSerializer
    http_method_names = ['get', 'post']
    lookup_field = 'account_tier_name__iexact'


class ImageUpload(viewsets.ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer
    http_method_names = ['post']
