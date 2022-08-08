from rest_framework import serializers
from .models import Users, AccountTiers, OriginalImages, ResizeImages
from .expires_and_resize_image import image_resizer, create_expires_image
from rest_framework.validators import UniqueTogetherValidator


class AccountTiersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AccountTiers
        fields = ('account_tier_name',
                  'link_to_the_originally_uploaded_file',
                  'ability_to_generate_expiring_links',
                  'image_height',)


class UsersSerializer(serializers.HyperlinkedModelSerializer):
    account_tier = serializers.SlugRelatedField(slug_field='account_tier_name',
                                                queryset=AccountTiers.objects.all())

    class Meta:
        model = Users
        fields = ('user_name', 'account_tier')

    def create(self, validated_data):
        account_tier = AccountTiers.objects.get(account_tier_name=validated_data['account_tier'])
        return Users.objects.create(user_name=validated_data['user_name'], account_tier=account_tier)


class UserImageSerializer(serializers.ModelSerializer):
    resize_images_list = serializers.SerializerMethodField()

    def get_resize_images_list(self, originalimages):
        image = originalimages.resizeimages_set.all()
        return ResizeImagesSerializer(instance=image,
                                      many=True,
                                      context={'request': self.context.get('request')}).data

    class Meta:
        model = OriginalImages
        fields = ('user', 'image_name', 'image', 'width', 'height', 'resize_images_list')

    def to_representation(self, obj):
        # get the original representation
        image_response = super(UserImageSerializer, self).to_representation(obj)
        # remove 'image' field if mobile request

        if not self.context.get('user').account_tier.link_to_the_originally_uploaded_file:
            image_response.pop('image')
        image_response.pop('user')

        return image_response


class ResizeImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResizeImages
        fields = ('width', 'height', 'resize_image')


class UploadImagesSerializer(serializers.ModelSerializer):
    resize_images_list = serializers.SerializerMethodField()

    def get_resize_images_list(self, originalimages):
        image = originalimages.resizeimages_set.all()
        return ResizeImagesSerializer(instance=image, many=True, context={'request': self.context.get('request')}).data

    class Meta:
        model = OriginalImages
        fields = ('user', 'image_name', 'image', 'resize_images_list')
        validators = [
            UniqueTogetherValidator(
                queryset=OriginalImages.objects.all(),
                fields=['user', 'image_name'],
                message="Image name must by unique"
            )
        ]

    def create(self, validated_data):
        original_image = OriginalImages.objects.create(**validated_data)

        size_list = validated_data['user'].account_tier.image_height
        for size in size_list:
            resize_image = image_resizer(image_to_resize=validated_data['image'], size=size)
            ResizeImages.objects.create(original_image=original_image, resize_image=resize_image)
        return original_image

    def to_representation(self, obj):
        # get the original representation
        image_response = super(UploadImagesSerializer, self).to_representation(obj)

        # remove 'image' field if mobile request
        if not Users.objects.get(pk=image_response['user']).account_tier.link_to_the_originally_uploaded_file:
            image_response.pop('image')
        image_response.pop('user')

        return image_response


class CheckUserHasImagePermissionsSerializer(serializers.ModelSerializer):

    user = serializers.SlugRelatedField(slug_field='user_name',
                                        queryset=Users.objects.all())

    original_image_name = serializers.CharField()

    def validate(self, value_to_valid):
        if not OriginalImages.objects.filter(user=value_to_valid['user'],
                                             image_name=value_to_valid['original_image_name']).exists():
            raise serializers.ValidationError("Image does not exist or does not belong to the user.")

        if not 300 <= value_to_valid['expiring_time'] <= 30000:
            raise serializers.ValidationError("Expiring time must between 300 and 30000")

        if not value_to_valid['user'].account_tier.ability_to_generate_expiring_links:
            raise serializers.ValidationError("The user has an inadequate account level to perform this operation")
        return value_to_valid

    class Meta:
        model = ResizeImages
        fields = ('user', 'original_image_name', 'expiring_time')

    def to_representation(self, response):
        # get the original representation
        # remove 'image' field if mobile request
        response['original_image'] = \
            OriginalImages.objects.values('pk').get(user=response['user'],
                                                    image_name=response['original_image_name'])['pk']

        return response


class ExpiresImagesSerializer(serializers.ModelSerializer):
    resize_image = serializers.ImageField(read_only=True)

    class Meta:
        model = ResizeImages
        fields = ('original_image', 'expiring_time', 'resize_image')

    def create(self, validated_data):
        expiring_time = validated_data['expiring_time']

        original_image = validated_data['original_image']

        expires_image = create_expires_image(original_image=original_image)

        return ResizeImages.objects.create(original_image=original_image,
                                           resize_image=expires_image,
                                           expiring_time=expiring_time)

    def to_representation(self, obj):
        # get the original representation
        image_response = super(ExpiresImagesSerializer, self).to_representation(obj)

        # remove 'image' field if mobile request
        image_response.pop('original_image')

        return image_response
