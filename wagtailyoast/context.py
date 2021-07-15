import os
import json
import pkg_resources
from django.conf import settings

# =======================================
# Context variables passed for javascript
# =======================================

try:
    #  Production part
    VERSION = pkg_resources.get_distribution("wagtailyoast").version
except pkg_resources.DistributionNotFound:
    #  Develop part
    with open(os.path.join(settings.BASE_DIR, 'package.json')) as package:
        data = json.load(package)
        VERSION = data['version']

LOCALE = settings.WY_LOCALE
STATIC_URL = settings.STATIC_URL
