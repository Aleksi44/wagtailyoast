import json
from django.utils.html import format_html, format_html_join, mark_safe
from django.templatetags.static import static
from wagtail.core import hooks

from . import context


@hooks.register('insert_editor_js')
def yoast_panel_js():
    cxt = json.dumps({
        'version': context.VERSION,
        'locale': context.LOCALE,
    })
    js_files = [
        'wagtailyoast/dist/js/yoastworker%s.js' % context.VERSION,
        'wagtailyoast/dist/js/yoastanalysis%s.js' % context.VERSION,
    ]
    js_includes = format_html_join(
        '\n',
        '<script src="{0}"></script>',
        ((static(filename),) for filename in js_files)
    )
    js_exec = format_html(
        "<script>{}</script>",
        mark_safe("$(function() {const panel = new Yoast.Panel(%s);panel.init();});" % cxt)
    )
    return js_includes + js_exec


@hooks.register('insert_editor_css')
def yoast_panel_css():
    css_files = [
        'wagtailyoast/dist/css/styles%s.css' % context.VERSION,
    ]
    css_includes = format_html_join(
        '\n',
        '<link href="{0}" rel="stylesheet" type="text/css">',
        ((static(filename),) for filename in css_files)
    )
    return css_includes
