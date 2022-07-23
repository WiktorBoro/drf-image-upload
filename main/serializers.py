from rest_framework import serializers
from .models import Users, AccountTiers, Images, Links
from .upload_image_and_create_links import UploadImage
from rest_framework.validators import UniqueValidator


class UsersSerializer(serializers.HyperlinkedModelSerializer):
    account_tier = serializers.CharField(source="account_tier.account_tier_name")

    class Meta:
        model = Users
        fields = ('user_name', 'account_tier',)


class AccountTiersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AccountTiers
        fields = ('account_tier_name',
                  'link_to_the_originally_uploaded_file',
                  'ability_to_generate_expiring_links',
                  'image_height',)


class ImagesSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(source='user.user_name',
                                              queryset=Users.objects.all(),
                                              many=False)
    image_name = serializers.CharField(max_length=50)
    image = serializers.ImageField()

    def create(self, validated_data):
        user = Users.objects.get(user_name=validated_data['user']['user_name'])
        image_name = validated_data['image_name']
        upload_image = UploadImage(user=user,
                                   original_image=validated_data['image'],
                                   image_name=image_name)
        upload_image.upload_original_image()
        upload_image.upload_links()

        return Links

