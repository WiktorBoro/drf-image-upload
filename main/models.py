from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from .models_validators import validate_image_height


class AccountTiers(models.Model):
    account_tier_name = models.CharField(max_length=50, unique=True)
    link_to_the_originally_uploaded_file = models.BooleanField(default=False)
    ability_to_generate_expiring_links = models.BooleanField(default=False)
    image_height = models.CharField(max_length=100,
                                    default="",
                                    validators=[validate_image_height])
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


class Images(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    image_name = models.CharField(max_length=50, unique=True)

    width = models.SmallIntegerField(null=True)
    height = models.SmallIntegerField(null=True)
    image = models.ImageField(height_field='height', width_field='width')

    objects = models.Manager()

    def __str__(self):
        return self.image_name


class Links(models.Model):
    images = models.ManyToManyField(Images)

    link = models.CharField(null=True, unique=True, max_length=50)

    expiring_time = models.SmallIntegerField(default=0,
                                             validators=[
                                                 MaxValueValidator(30000),
                                                 MinValueValidator(300)
                                             ])

    objects = models.Manager()
