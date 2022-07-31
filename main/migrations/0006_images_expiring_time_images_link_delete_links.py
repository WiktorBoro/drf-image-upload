# Generated by Django 4.0.6 on 2022-07-25 19:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_images_image_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='images',
            name='expiring_time',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(30000), django.core.validators.MinValueValidator(300)]),
        ),
        migrations.AddField(
            model_name='images',
            name='link',
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
        migrations.DeleteModel(
            name='Links',
        ),
    ]
