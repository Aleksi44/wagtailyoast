#!/usr/bin/env python
import os
from setuptools import find_packages, setup
import json

PROJECT_DIR = os.path.dirname(__file__)

with open("README.rst", "r") as fh:
    long_description = fh.read()

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
    long_description=long_description,
    long_description_content_type='text/x-rst',
    keywords="wagtail yoast seo",
    license='GPL-3.0',
    install_requires=[
        'Django>=4.2',
        'wagtail>=5.2',
    ],
    python_requires='>=3.9',
    packages=find_packages(
        exclude=['test_app', 'test_app.*', 'tests', 'tests.*'],
    ),
    include_package_data=True,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 4.2',
        'Framework :: Django :: 5.0',
        'Framework :: Django :: 5.1',
        'Framework :: Django :: 5.2',
        'Framework :: Wagtail',
        'Framework :: Wagtail :: 5',
        'Framework :: Wagtail :: 6',
        'Framework :: Wagtail :: 7',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: Software Development'
    ]
)
