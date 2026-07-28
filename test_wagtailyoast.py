"""Smoke tests for the wagtailyoast package.

These cover the import chain Wagtail exercises at startup
(``wagtail_hooks`` -> ``context``) and the two editor hooks. VERSION is
interpolated into the static asset filenames, so a wrong value does not
just mislabel the package - it 404s the editor's JS and CSS.

Run with:

    python -m django test --settings=test_settings
"""
import importlib
import json
import os
from importlib.metadata import version as installed_version
from unittest import mock

from django.conf import settings
from django.test import SimpleTestCase

from wagtailyoast import context, wagtail_hooks
from wagtailyoast.edit_handlers import YoastPanel


class ContextTests(SimpleTestCase):

    def test_version_matches_installed_distribution(self):
        self.assertEqual(context.VERSION, installed_version("wagtailyoast"))

    def test_locale_comes_from_settings(self):
        self.assertEqual(context.LOCALE, settings.WY_LOCALE)

    def test_static_url_comes_from_settings(self):
        self.assertEqual(context.STATIC_URL, settings.STATIC_URL)

    def test_package_json_fallback_when_distribution_is_missing(self):
        """The develop-mode path: no installed distribution -> package.json."""
        from importlib.metadata import PackageNotFoundError

        with mock.patch(
            "importlib.metadata.version",
            side_effect=PackageNotFoundError("wagtailyoast"),
        ):
            reloaded = importlib.reload(context)
            with open(os.path.join(settings.BASE_DIR, "package.json")) as f:
                expected = json.load(f)["version"]
            self.assertEqual(reloaded.VERSION, expected)

        # Restore the real module state for the other tests.
        importlib.reload(context)


class EditorHookTests(SimpleTestCase):

    def test_js_hook_includes_versioned_worker_and_analysis_scripts(self):
        html = wagtail_hooks.yoast_panel_js()
        self.assertIn("yoastworker%s.js" % context.VERSION, html)
        self.assertIn("yoastanalysis%s.js" % context.VERSION, html)

    def test_js_hook_passes_context_to_the_panel(self):
        html = wagtail_hooks.yoast_panel_js()
        self.assertIn("new Yoast.Panel(", html)
        self.assertIn(json.dumps(context.VERSION), html)
        self.assertIn(json.dumps(context.LOCALE), html)

    def test_css_hook_includes_versioned_stylesheet(self):
        html = wagtail_hooks.yoast_panel_css()
        self.assertIn("styles%s.css" % context.VERSION, html)


class YoastPanelTests(SimpleTestCase):

    def test_panel_instantiates_with_defaults(self):
        panel = YoastPanel()
        self.assertEqual(panel.heading, "Yoast")
        self.assertEqual(panel.title_field, "seo_title")
        self.assertEqual(panel.search_description, "search_description")
        self.assertEqual(panel.slug, "slug")

    def test_clone_kwargs_round_trips_custom_fields(self):
        panel = YoastPanel(
            keywords="kw", title="custom_title",
            search_description="custom_desc", slug="custom_slug",
        )
        kwargs = panel.clone_kwargs()
        self.assertEqual(kwargs["title"], "custom_title")
        self.assertEqual(kwargs["search_description"], "custom_desc")
        self.assertEqual(kwargs["slug"], "custom_slug")
