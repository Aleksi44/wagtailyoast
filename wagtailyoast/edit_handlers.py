from django import forms
from wagtail.admin.edit_handlers import ObjectList
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel


class YoastPanel(ObjectList):
    template = "wagtailyoast/edit_handlers/yoast_panel.html"

    def __init__(self, keywords='keywords', title='seo_title', search_description='search_description', slug='slug', heading='Yoast',
                 *args, **kwargs):
        #  TODO: Test if fields exist

        self.title_field = title
        self.search_description = search_description
        self.slug = slug

        children = [
            MultiFieldPanel([
                FieldPanel(keywords, widget=forms.TextInput(attrs={'id': 'yoast_keywords'})),
            ], heading="Page")
        ]
        super().__init__(children=children, heading=heading)
