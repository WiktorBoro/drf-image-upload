# Generated by Django 4.0.6 on 2022-07-31 17:07

from django.db import migrations
import main.custom_models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_resizeimages_image_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resizeimages',
            name='image_name',
        ),
        migrations.AlterField(
            model_name='accounttiers',
            name='image_height',
            field=main.custom_models.IntegerListField(max_length=255),
        ),
    ]
