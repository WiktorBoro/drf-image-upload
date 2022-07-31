from rest_framework import serializers
from .models import Users, AccountTiers, OriginalImages, ResizeImages
from .resize_image import image_resizer, create_expires_image


class UsersSerializer(serializers.HyperlinkedModelSerializer):
    account_tier = serializers.PrimaryKeyRelatedField(source='account_tier.account_tier_name',
                                                      queryset=AccountTiers.objects.all())

    class Meta:
        model = Users
        fields = ('user_name', 'account_tier')

    def create(self, validated_data):
        account_tier = AccountTiers.objects.get(account_tier_name=validated_data['account_tier']['account_tier_name'])
        return Users.objects.create(user_name=validated_data['user_name'], account_tier=account_tier)


class AccountTiersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AccountTiers
        fields = ('account_tier_name',
                  'link_to_the_originally_uploaded_file',
                  'ability_to_generate_expiring_links',
                  'image_height',)


class ResizeImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResizeImages
        fields = ('width', 'height', 'resize_image')


class ExpiresImagesSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(source='original_image.user.user_name',
                                              queryset=Users.objects.all())
    image_name = serializers.CharField()

    class Meta:
        model = ResizeImages
        fields = ('user', 'image_name', 'expiring_time')

    def create(self, validated_data):
        user = Users.objects.get(user_name=validated_data['user'])
        expiring_time = validated_data['expiring_time']
        image = OriginalImages.objects.get(user=user, image_name=validated_data['image_name'])
        expires_image = create_expires_image(original_image=image)

        return ResizeImages.objects.create(original_image=image,
                                           resize_image=expires_image,
                                           expiring_time=expiring_time)


class OriginalImagesSerializer(serializers.ModelSerializer):
    resize_images_list = serializers.SerializerMethodField()

    def get_resize_images_list(self, originalimages):
        image = originalimages.resizeimages_set.all()
        return ResizeImagesSerializer(instance=image, many=True, context={'request': self.context.get('request')}).data

    class Meta:
        model = OriginalImages
        fields = ('user', 'image_name', 'image', 'resize_images_list')

    def create(self, validated_data):
        original_image = OriginalImages.objects.create(**validated_data)

        size_list = validated_data['user'].account_tier.image_height
        for size in size_list:
            resize_image = image_resizer(image_to_resize=validated_data['image'], size=size)
            ResizeImages.objects.create(original_image=original_image, resize_image=resize_image)
        return original_image
