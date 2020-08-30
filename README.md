# Wagtail Yoast SEO

[Yoastseo](https://github.com/Yoast/javascript/tree/master/packages/yoastseo) + [Wagtail](https://github.com/wagtail/wagtail) = 🚀

Tested with :

- django==3.0.9
- wagtail==2.10.1
- yoastseo:1.80.0

![Wagtail Yoast Screenshot](https://d271q0ph7te9f8.cloudfront.net/www/images/screenshot-wagtail-yoast-.original.png)


## Setup
--------

Install with pip : `pip install wagtailyoast`

Add wagtailyoast to django apps installed :

```
INSTALLED_APPS = [
    ...
    'wagtailyoast',
]
```

Add locale used for Yoast in your `settings.py` :

```
WY_LOCALE = 'en_US'
```

Add YoastPannel to your Page models :

```
from wagtail.admin.edit_handlers import TabbedInterface, ObjectList
from wagtailyoast.edit_handlers import YoastPanel


class TestPage(Page):
    ...
    keywords = models.CharField(default='', blank=True, max_length=100)

    edit_handler = TabbedInterface([
        ObjectList(Page.content_panels, heading=('Content')),
        ObjectList(Page.promote_panels, heading=('Promotion')),
        ObjectList(Page.settings_panels, heading=('Settings')),
        YoastPanel(
            keywords='keywords',
            title='seo_title',
            search_description='search_description',
            slug='slug'
        ),
    ])
```

`YoastPanel` params are :

- `keywords` : Default keywords of the page.
- `title` : 'Search Engine Friendly' title. This will appear at the top of the browser window.
- `search_description` : 'Search Engine Friendly' description.
- `slug` : URL of the page.

        
## Development env
---------------

```
git clone git@github.com:Aleksi44/wagtailyoast.git
```

### Run Django Server

```
python manage.py migrate --settings='settings'
python manage.py init --settings=settings
python manage.py runserver 0.0.0.0:4243 --settings='settings'
```

### Run Webpack Server

```
yarn
yarn start
```

