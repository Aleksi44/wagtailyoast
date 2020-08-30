#!/usr/bin/env python
import os
import sys
from setuptools import find_packages, setup
import json


PROJECT_DIR = os.path.dirname(__file__)

sys.path.append(os.path.join(PROJECT_DIR, 'src'))

with open('./package.json') as package:
    data = json.load(package)
    version = data['version']


setup(
    name='wagtailyoast',
    version=version,
    url='https://github.com/Aleksi44/wagtailyoast',
    author="Alexis Le Baron",
    author_email="alexis@stationspatiale.com",
    description="Yoast For Wagtail",
    keywords="wagtail yoast seo",
    license='GPL-3.0',
    install_requires=[
        'django==3.0.9',
        'wagtail==2.10.1',
    ],
    platforms=['linux'],
    packages=find_packages(),
    include_package_data=True,
)
