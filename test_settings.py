"""Minimal settings for running the wagtailyoast test suite.

Deliberately independent from settings.py, which configures the manual
demo project (the ``tests`` app) rather than an automated test run.
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DEBUG = True
SECRET_KEY = "test-only-secret-key"
USE_TZ = True

# The suite itself is SimpleTestCase-only, but Wagtail 5.2's system
# checks run a real ContentType query (GroupPagePermission.check ->
# _migrate_permission_type), so a connectable database must exist.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    },
}

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.staticfiles",
    "wagtail",
    "wagtail.admin",
    "wagtail.users",
    "wagtail.sites",
    "wagtailyoast",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
    },
]

STATIC_URL = "/static/"

WY_LOCALE = "en_US"
