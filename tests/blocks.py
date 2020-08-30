import requests
from io import BytesIO
from django.core.files.images import ImageFile
from wagtail.images.blocks import ImageChooserBlock
from wagtail.core.blocks import RichTextBlock
from wagtail.images.models import Image

from . import constants


class TextBlock(RichTextBlock):
    def __init__(self, **kwargs):
        super().__init__(features=constants.RICH_TEXT_FEATURES, **kwargs)

    def mock(self, content):
        return {
            'type': 'text',
            'value': content
        }


class ImageBlock(ImageChooserBlock):
    def mock(self, title):
        url = constants.URL_IMAGE_MOCK_1
        filename = "%s.png" % title
        try:
            ret = Image.objects.get(title=title)
        except Image.DoesNotExist:
            response = requests.get(url)
            file = ImageFile(BytesIO(response.content), name=filename)
            ret = Image(
                title=title,
                file=file
            )
            ret.save()
        return {
            'type': 'image',
            'value': ret.id
        }
