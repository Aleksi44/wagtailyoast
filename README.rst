*****************
Wagtail Yoast SEO
*****************

.. image:: https://img.shields.io/pypi/v/wagtailyoast
    :target: https://pypi.org/project/wagtailyoast/

.. image:: https://img.shields.io/pypi/pyversions/wagtailyoast
    :target: https://pypi.org/project/wagtailyoast/

`Yoastseo <https://github.com/Yoast/javascript/tree/master/packages/yoastseo>`_ + `Wagtail <https://github.com/wagtail/wagtail>`_ = 🚀

Requirements
############

- Python 3.9+
- Django 4.2+
- Wagtail 5.2+

Continuously tested against Wagtail 5.2, 6.3 and 7.x on Python 3.9 to
3.13. Bundles yoastseo 1.80.0.

Setup
#####

Install with pip :

``pip install wagtailyoast``

Add wagtailyoast to django apps installed :
::

    INSTALLED_APPS = [
        ...
        'wagtailyoast',
    ]

Add locale used for Yoast and make sure you have STATIC_URL set up in your `settings.py` :
::

    WY_LOCALE = 'en_US'
    STATIC_URL = '/static/'


Add YoastPannel to your Page models :

::

    from wagtail.admin.panels import TabbedInterface, ObjectList
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


`YoastPanel` params are :

- `keywords` : Default keywords of the page.
- `title` : 'Search Engine Friendly' title. This will appear at the top of the browser window.
- `search_description` : 'Search Engine Friendly' description.
- `slug` : URL of the page.


Development env
###############

::

    git clone git@github.com:Aleksi44/wagtailyoast.git
    pip install -r requirements.txt


Run Django Server
*****************

::

    python manage.py migrate
    python manage.py init
    python manage.py runserver 0.0.0.0:4243


Run Webpack Server
******************

::

    yarn
    yarn start


Changelog
#########

0.0.11 (unreleased)
*******************

- Fix ``ModuleNotFoundError: No module named 'pkg_resources'`` at Django
  startup on setuptools 82 and later, which removed ``pkg_resources``.
- Fix the panel not rendering on Wagtail 4.0 and later: the panels API
  introduced there ignores the legacy class-level ``template``
  attribute, so the panel silently degraded to a plain ``ObjectList``.
- Fix the panel stylesheet never loading: it was registered on
  ``insert_editor_css``, a hook Wagtail no longer renders.
- Fix a custom ``keywords`` field being discarded when Wagtail clones
  the panel, which raised ``FieldError`` on models without a field of
  that literal name.
- Declare runtime dependencies. ``install_requires`` was empty, so
  ``pip install wagtailyoast`` pulled in neither Django nor Wagtail and
  the package failed at import.
- Declare ``python_requires`` and refresh the trove classifiers, which
  advertised Python 3.6-3.8 while the package is tested on 3.9-3.13.
- Stop shipping every previous release's JavaScript and CSS: packages
  contained the built assets of all versions since 0.0.1, roughly 39 MB
  where one version's assets are about 5 MB.
- Add a test suite and continuous integration across Wagtail 5.2, 6.3
  and 7.x on Python 3.9 to 3.13.

