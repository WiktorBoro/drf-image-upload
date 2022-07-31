from django.core.exceptions import ValidationError
from django.db import models
import os
from uuid import uuid4
from django.utils.deconstruct import deconstructible


@deconstructible
class CreateName(object):

    def __init__(self, sub_path=''):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.path, filename)


def validate_image_height(value):
    for height in value.split(','):
        try:
            int(height)
        except ValueError:
            raise ValidationError("The heights must be numbers written after ,")
    return value


class IntegerListField(models.CharField):

    description = 'list of integers'

    def from_db_value(self, value, expression, connection):
        if value is None:
            return None
        return list(map(int, value.split(',')))

    def to_python(self, value):
        if isinstance(value, list):
            return value
        if value is None:
            return None
        return list(map(int, value.split(',')))

    def get_prep_value(self, value):
        if value is None:
            return None
        return value
