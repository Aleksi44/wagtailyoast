import os
import json
from importlib.metadata import PackageNotFoundError, version

from django.conf import settings

# =======================================
# Context variables passed for javascript
# =======================================

try:
    #  Production part
    VERSION = version("wagtailyoast")
except PackageNotFoundError:
    #  Develop part
    with open(os.path.join(settings.BASE_DIR, 'package.json')) as package:
        data = json.load(package)
        VERSION = data['version']

LOCALE = settings.WY_LOCALE
STATIC_URL = settings.STATIC_URL
