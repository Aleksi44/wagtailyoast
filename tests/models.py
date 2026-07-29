from django.db import models
from django.utils.translation import gettext_lazy
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.admin.panels import TabbedInterface, ObjectList

from wagtailyoast.edit_handlers import YoastPanel

from .blocks import TextBlock, ImageBlock


# =================================
# TestPage used for testing purpose
# =================================


class TestPage(Page):
    body = StreamField([
        ('text', TextBlock()),
        ('image', ImageBlock()),
    ], blank=True, use_json_field=True)
    keywords = models.CharField(default='', blank=True, max_length=100)

    edit_handler = TabbedInterface([
        ObjectList(
            Page.content_panels + [FieldPanel('body')],
            heading=gettext_lazy('Content')
        ),
        ObjectList(Page.promote_panels, heading=gettext_lazy('Promotion')),
        ObjectList(Page.settings_panels, heading=gettext_lazy('Settings')),
        YoastPanel(
            keywords='keywords',
            title='seo_title',
            search_description='search_description',
            slug='slug'
        ),
    ])
