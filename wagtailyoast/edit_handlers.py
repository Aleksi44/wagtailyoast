from django import forms
from wagtail.admin.edit_handlers import ObjectList
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel


class YoastPanel(ObjectList):
    template = "wagtailyoast/edit_handlers/yoast_panel.html"

    def __init__(self, keywords='keywords', title='seo_title',
                 search_description='search_description', slug='slug',
                 heading='Yoast', *args, **kwargs):
        """
        Panel used by a wagtail Page

        :param keywords: Default keywords of the page.
        :param title: 'Search Engine Friendly' title.
        :param search_description: 'Search Engine Friendly' description.
        :param slug: URL of the page.
        :param heading: Heading of pannel
        """
        #  TODO: Test if fields exist

        self.title_field = title
        self.search_description = search_description
        self.slug = slug

        children = [
            MultiFieldPanel([
                FieldPanel(
                    keywords,
                    widget=forms.TextInput(attrs={'id': 'yoast_keywords'})
                ),
            ], heading="Page")
        ]
        super().__init__(children=children, heading=heading)

    def clone_kwargs(self):
        kwargs = super().clone_kwargs()
        kwargs['title'] = self.title_field
        kwargs['search_description'] = self.search_description
        kwargs['slug'] = self.slug
        return kwargs
