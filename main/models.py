from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from .custom_models import IntegerListField, validate_image_height, CreateName


class AccountTiers(models.Model):
    account_tier_name = models.CharField(max_length=50, unique=True)
    link_to_the_originally_uploaded_file = models.BooleanField(default=False)
    ability_to_generate_expiring_links = models.BooleanField(default=False)

    image_height = IntegerListField(max_length=255, validators=[validate_image_height])
    objects = models.Manager()

    def __str__(self):
        return self.account_tier_name


class Users(models.Model):
    user_name = models.CharField(max_length=50, unique=True)
    account_tier = models.ForeignKey(AccountTiers,
                                     on_delete=models.SET_DEFAULT,
                                     default="")
    objects = models.Manager()

    def __str__(self):
        return self.user_name


class OriginalImages(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    image_name = models.CharField(max_length=50)

    width = models.SmallIntegerField(null=True)
    height = models.SmallIntegerField(null=True)

    image = models.ImageField(upload_to=CreateName(), height_field='height', width_field='width')

    objects = models.Manager()

    def __str__(self):
        return self.image_name


class ResizeImages(models.Model):

    original_image = models.ForeignKey(OriginalImages, on_delete=models.CASCADE)

    width = models.SmallIntegerField(null=True)
    height = models.SmallIntegerField(null=True)

    resize_image = models.ImageField(upload_to=CreateName(), height_field='height', width_field='width')

    expiring_time = models.SmallIntegerField(default=0,
                                             validators=[
                                                 MaxValueValidator(30000),
                                                 MinValueValidator(300)
                                             ])
    objects = models.Manager()

    def __str__(self):
        return str(self.original_image) + ' - ' + str(self.height) + 'x' + str(self.width)
