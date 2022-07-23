from django.core.exceptions import ValidationError


def validate_image_height(value):
    for height in value.split(','):
        try:
            int(height)
        except ValueError:
            raise ValidationError("The heights must be numbers written after ,")
    return value
