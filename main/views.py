from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404
from .serializers import UsersSerializer, \
    AccountTiersSerializer, \
    UploadImagesSerializer, \
    ExpiresImagesSerializer, \
    UserImageSerializer
from .models import Users, AccountTiers, OriginalImages
from rest_framework.response import Response
from .expires_and_resize_image import del_expires_image


class AccountTiersView(viewsets.ModelViewSet):
    queryset = AccountTiers.objects.all()
    serializer_class = AccountTiersSerializer
    http_method_names = ['get', 'post']
    lookup_field = 'account_tier_name__iexact'


class UserImageView(viewsets.ViewSet):
    lookup_field = 'user_name'
    serializer_class = UsersSerializer

    def list(self, request):
        queryset = Users.objects.all()
        serializer_user = UsersSerializer(queryset, many=True)
        return Response(serializer_user.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer_user = UsersSerializer(data=request.data)

        if not serializer_user.is_valid():
            return Response(serializer_user.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer_user.save()
        return Response(serializer_user.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, user_name=None):
        user = get_object_or_404(Users, user_name=user_name)

        queryset = OriginalImages.objects.filter(user=user)

        if not queryset:
            return Response("User don't have image", status=status.HTTP_400_BAD_REQUEST)

        serializer_user_image_list = UserImageSerializer(queryset, many=True, context={'request': request,
                                                                                       'user': user})

        return Response(serializer_user_image_list.data, status=status.HTTP_200_OK)


class ImageUpload(viewsets.ViewSet):
    serializer_class = UploadImagesSerializer

    def create(self, request):
        serializer_original_image = UploadImagesSerializer(data=request.data, context={'request': request})

        if not serializer_original_image.is_valid():
            return Response(serializer_original_image.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer_original_image.save()

        return Response(serializer_original_image.data, status=status.HTTP_201_CREATED)


class ExpiresImages(viewsets.ViewSet):
    serializer_class = ExpiresImagesSerializer

    def create(self, request):
        # print(request.data)
        expires_images_serializer = ExpiresImagesSerializer(data=request.data,
                                                            context={'request': request})

        if not expires_images_serializer.is_valid():
            return Response(expires_images_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        print(expires_images_serializer)

        expires_images_serializer.save()
        expiring_time = expires_images_serializer.data['expiring_time']
        resize_image = expires_images_serializer.data['resize_image']
        del_expires_image.delay(expiring_time=expiring_time, image=resize_image)
        # print(expires_images_serializer.data)
        return Response(expires_images_serializer.data, status=status.HTTP_201_CREATED)
