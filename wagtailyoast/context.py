import pkg_resources
from django.conf import settings

# Version

try:
    VERSION = pkg_resources.get_distribution("wagtailyoast").version
except pkg_resources.DistributionNotFound:
    #  Develop part
    import os
    import json
    from django.conf import settings

    with open(os.path.join(settings.BASE_DIR, 'package.json')) as package:
        data = json.load(package)
        VERSION = data['version']

LOCALE = settings.WY_LOCALE
