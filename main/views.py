from rest_framework import viewsets, status
from rest_framework.views import APIView
from .serializers import UsersSerializer, AccountTiersSerializer, OriginalImagesSerializer, ExpiresImagesSerializer
from .models import Users, AccountTiers, OriginalImages
from rest_framework.response import Response
from .resize_image import del_expires_image


class UsersView(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    http_method_names = ['get', 'post']


class AccountTiersView(viewsets.ModelViewSet):
    queryset = AccountTiers.objects.all()
    serializer_class = AccountTiersSerializer
    http_method_names = ['get', 'post']
    lookup_field = 'account_tier_name__iexact'


class ImageUpload(viewsets.ViewSet):
    serializer_class = OriginalImagesSerializer

    def create(self, request):
        # queryset = OriginalImages.objects.all()
        serializer_original_image = OriginalImagesSerializer(data=request.data, context={'request': request})

        if not serializer_original_image.is_valid():
            return Response(serializer_original_image.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer_original_image.save()

        print(serializer_original_image.data)

        return Response(serializer_original_image.data, status=status.HTTP_201_CREATED)


class ExpiresImages(viewsets.ViewSet):
    serializer_class = ExpiresImagesSerializer

    def create(self, request):
        expires_images_serializer = OriginalImagesSerializer(data=request.data, context={'request': request})

        if not expires_images_serializer.is_valid():
            return Response(expires_images_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        print(expires_images_serializer)
        expires_images_serializer.save()
        expiring_time = expires_images_serializer.data['expiring_time']
        resize_image = expires_images_serializer.data['resize_image']
        del_expires_image.delay(expiring_time=expiring_time, image=resize_image)

        return Response(expires_images_serializer.data, status=status.HTTP_201_CREATED)
