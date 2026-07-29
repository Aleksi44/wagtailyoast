"""URLconf for the test suite: just the Wagtail admin."""
from django.urls import include, path

from wagtail.admin import urls as wagtailadmin_urls

urlpatterns = [
    path("admin/", include(wagtailadmin_urls)),
]
