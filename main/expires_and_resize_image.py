from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from celery import shared_task
from time import sleep
from .models import ResizeImages


def image_resizer(image_to_resize, size):
    image_to_resize = Image.open(image_to_resize)

    img_format = image_to_resize.format
    old_width, old_height = image_to_resize.size

    new_height = int(size)
    new_width = int(new_height / old_height * old_width)

    image_to_resize = image_to_resize.resize((new_width, new_height))
    resize_image = BytesIO()

    image_to_resize.save(fp=resize_image, format=img_format, quality=100)
    # END pillow operation

    # Prepared the image to be saved in db and saved
    resize_image = ContentFile(resize_image.getvalue(), name='none.' + img_format.lower())

    return resize_image


def create_expires_image(original_image):
    image_to_binar = Image.open(original_image.image)
    image = image_to_binar.convert('1')
    img_to_save = BytesIO()
    img_format = image_to_binar.format

    image.save(fp=img_to_save, format=image.format.lower(), quality=100)
    # END pillow operation

    # Prepared the image to be saved in db and saved
    img_to_save = ContentFile(img_to_save.getvalue(), name='none.' + img_format.lower())
    return img_to_save


@shared_task(bind=True)
def del_expires_image(expiring_time: int,
                      image: object):
    sleep(expiring_time)
    expiring_image = ResizeImages.objects.get(expiring_time=expiring_time, resize_image=image)
    expiring_image.image.delete(save=True)
    expiring_image.delete()
