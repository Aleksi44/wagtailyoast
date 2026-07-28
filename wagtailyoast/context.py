import os
import json
from django.conf import settings

try:  # Python 3.8+
    from importlib.metadata import PackageNotFoundError, version
except ImportError:  # Python < 3.8
    from pkg_resources import DistributionNotFound as PackageNotFoundError
    from pkg_resources import get_distribution

    def version(distribution_name):
        return get_distribution(distribution_name).version

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
