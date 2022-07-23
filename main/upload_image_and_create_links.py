from secrets import token_hex
from django.conf import settings
from .models import Links, Images
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile


class UploadImage:

    def __init__(self,
                 user,
                 original_image,
                 image_name):
        self.original_image = original_image
        self.user = user
        self.image_name = image_name

    def generate_link(self) -> str:
        domain = '127.0.0.1:8000'
        nbytes_url_code = 16
        protocol_http_https = "http://"

        hex_token = token_hex(nbytes=nbytes_url_code)
        link = f'{protocol_http_https}{domain}{settings.MEDIA_URL}{hex_token}'
        return link, hex_token

    def upload_original_image(self):
        original_image = Images(user=self.user,
                                image=self.original_image,
                                image_name=self.image_name)
        original_image.save()

    def check_user_have_permissions_to_size(self):
        pass

    def resize_image(self,
                     size):
        image_to_resize = Image.open(self.original_image)
        img_format = image_to_resize.format
        old_width, old_height = image_to_resize.size

        new_height = int(size)
        new_width = int(new_height / old_height * old_width)

        image_to_resize = image_to_resize.resize((new_width, new_height))
        img_to_save = BytesIO()

        image_to_resize.save(fp=img_to_save, format=img_format, quality=100)
        # END pillow operation

        link_resize_img, hex_token = self.generate_link()

        # Prepared the image to be saved in db and saved
        img_to_save = ContentFile(img_to_save.getvalue(), name=hex_token+'.'+img_format.lower())

        return img_to_save, link_resize_img

    def upload_links(self):
        sizes_to_generating_url = self.user.account_tier.image_height

        # If user have required account tier we add original size to generate link
        if self.user.account_tier.link_to_the_originally_uploaded_file:
            Links(link=self.generate_link(), images=self.original_image)

        # We iterate over all the sizes to be generated
        for size in sizes_to_generating_url.replace(' ', '').split(','):

            img_to_save, link_resize_img = self.resize_image(size)

            resize_img = Images(image=img_to_save,
                                image_name=self.image_name + " - " + size,
                                user=self.user)

            resize_img.save()
            link = Links(link=link_resize_img)
            link.save()
            link.images.add(Images.objects.get(image_name=self.image_name, user=self.user), resize_img)
