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
from django.contrib.auth.models import AnonymousUser
from django.db import models
from django.test import RequestFactory, SimpleTestCase

from wagtail.models import Page

from wagtailyoast import context, wagtail_hooks
from wagtailyoast.edit_handlers import YoastPanel


class ProbeModel(models.Model):
    """Minimal model exposing the `keywords` field YoastPanel expects.

    Test-only; never migrated or saved. A plain model (not a Page
    subclass) keeps the migration-less test app out of Django's
    migration state, and the panel machinery is model-agnostic.
    """

    keywords = models.CharField(max_length=255, blank=True, default="")

    class Meta:
        app_label = "wagtailyoast"


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

    def test_hooks_are_registered_on_hooks_wagtail_still_renders(self):
        """`insert_editor_css` is no longer rendered by any Wagtail
        template, so registering the stylesheet there loaded nothing."""
        from wagtail import hooks

        css_hooks = hooks.get_hooks("insert_global_admin_css")
        self.assertIn(wagtail_hooks.yoast_panel_css, css_hooks)

        js_hooks = hooks.get_hooks("insert_editor_js")
        self.assertIn(wagtail_hooks.yoast_panel_js, js_hooks)


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


class YoastPanelRenderTests(SimpleTestCase):
    """The panel must render its own template, not a plain ObjectList.

    Wagtail's post-4.0 panels API ignores the legacy class-level
    `template` attribute, which left the panel rendering as a bare
    ObjectList (no #yoast_panel markup for the JS to attach to) on
    every modern Wagtail - the breakage reported in issue #8.
    """

    def _bound_panel(self):
        panel_def = YoastPanel().bind_to_model(ProbeModel)
        form_class = panel_def.get_form_class()
        instance = ProbeModel()
        form = form_class(instance=instance)
        request = RequestFactory().get("/")
        request.user = AnonymousUser()
        return panel_def.get_bound_panel(
            instance=instance, request=request, form=form,
        )

    def test_bound_panel_uses_the_yoast_template(self):
        bound = self._bound_panel()
        self.assertEqual(
            bound.template_name,
            "wagtailyoast/edit_handlers/yoast_panel.html",
        )

    def test_rendered_panel_contains_the_yoast_markup(self):
        html = str(self._bound_panel().render_html({}))
        self.assertIn('id="yoast_panel"', html)
        self.assertIn('id="yoast_title" data-field="seo_title"', html)
        self.assertIn(
            'id="yoast_search_description"'
            ' data-field="search_description"',
            html,
        )
        self.assertIn('id="yoast_slug" data-field="slug"', html)
        self.assertIn('id="yoast_results_seo"', html)
        self.assertIn('id="yoast_results_readability"', html)

    def test_rendered_panel_contains_the_keywords_form_field(self):
        html = str(self._bound_panel().render_html({}))
        self.assertIn('id="yoast_keywords"', html)

    def test_clone_preserves_a_custom_keywords_field(self):
        """clone_kwargs dropped `keywords`, so binding rebuilt the
        panel against the default field name and crashed on any model
        without a literal `keywords` field."""
        panel_def = YoastPanel(keywords="seo_title").bind_to_model(Page)
        form_class = panel_def.get_form_class()
        self.assertIn("seo_title", form_class.base_fields)
