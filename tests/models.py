from django.db import models
from django.utils.translation import gettext_lazy
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.admin.edit_handlers import TabbedInterface, ObjectList

from wagtailyoast.edit_handlers import YoastPanel

from .blocks import TextBlock, ImageBlock


class TestPage(Page):
    body = StreamField([
        ('text', TextBlock()),
        ('image', ImageBlock()),
    ], blank=True)
    keywords = models.CharField(default='', blank=True, max_length=100)

    edit_handler = TabbedInterface([
        ObjectList(Page.content_panels + [StreamFieldPanel('body')], heading=gettext_lazy('Content')),
        ObjectList(Page.promote_panels, heading=gettext_lazy('Promotion')),
        ObjectList(Page.settings_panels, heading=gettext_lazy('Settings')),
        YoastPanel(
            keywords='keywords',
            title='seo_title',
            search_description='search_description',
            slug='slug'
        ),
    ])
