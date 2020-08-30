import json
from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from wagtail.core.models import Page, Site
from wagtail.images.models import Image

from tests.models import TestPage
from tests.blocks import TextBlock, ImageBlock
from tests import constants


class Command(BaseCommand):

    def handle(self, *args, **options):
        Site.objects.all().delete()
        Page.objects.all().delete()
        Image.objects.all().delete()

        text = TextBlock()
        image = ImageBlock()

        # Create admin user

        user, created = User.objects.get_or_create(
            username='wagtail',
            first_name='User',
            last_name='Admin',
            email='test@test.test',
            is_staff=True,
            is_superuser=True,
            is_active=True
        )
        if created:
            user.save()
            user.set_password('yoast')
            for group in Group.objects.all():
                user.groups.add(group)
            user.save()

        #  RootPage, HomePage, Site

        page_content_type, created = ContentType.objects.get_or_create(
            model='page',
            app_label='wagtailcore'
        )

        root = Page.objects.create(
            title="Root",
            slug='root',
            content_type=page_content_type,
            path='0001',
            depth=1,
            numchild=1,
            url_path='/',
        )
        root.save()

        home_page = TestPage.objects.create(
            title="Examples - Test page",
            slug='home',
            path='00010001',
            depth=2,
            numchild=0,
            body=json.dumps([
                text.mock(constants.WELCOME_TEXT),
            ])
        )
        home_page.save()

        site = Site.objects.create(
            hostname='localhost',
            port=8080,
            root_page_id=home_page.id,
            is_default_site=True
        )
        site.save()

        # -------------------------------- Examples --------------------------------

        # Goal : get perfect score with yoast

        content_page = TestPage(
            title="Example 1 - PerfectPage",
            seo_title="perfect yoast page",
            search_description="perfect yoast page",
            slug='perfect',
            keywords='perfect yoast page',
            body=json.dumps([
                text.mock(constants.TEXT_1),
                image.mock('perfect yoast page'),
                text.mock(constants.TEXT_1),
            ])
        )
        home_page.add_child(instance=content_page)

        content_page = TestPage(
            title="Example 2 - EmptyPage",
            seo_title="",
            search_description="",
            slug='empty',
            body=json.dumps([
            ])
        )
        home_page.add_child(instance=content_page)
