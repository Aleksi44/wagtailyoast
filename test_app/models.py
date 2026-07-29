"""Minimal page type for the admin integration tests.

Test-only: gives the admin edit view a real page whose edit handler
includes YoastPanel, so the tests can assert on what Wagtail actually
renders rather than on a panel rendered in isolation.
"""
from django.db import models

from wagtail.admin.panels import ObjectList, TabbedInterface
from wagtail.models import Page

from wagtailyoast.edit_handlers import YoastPanel


class YoastTestPage(Page):
    keywords = models.CharField(max_length=255, blank=True, default="")

    edit_handler = TabbedInterface([
        ObjectList(Page.content_panels, heading="Content"),
        YoastPanel(),
        ObjectList(Page.promote_panels, heading="Promote"),
    ])
