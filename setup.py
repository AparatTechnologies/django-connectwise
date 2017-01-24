#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import djconnectwise

LONG_DESCRIPTION = open('README.md').read()

setup(
    name="django-connectwise",
    version=djconnectwise.__version__,
    description='Django app for working with ConnectWise. Defines models (tickets, members, companies, etc.) '
    'and callbacks.',
    long_description=LONG_DESCRIPTION,
    keywords='django connectwise rest api python',
    packages=find_packages(),
    author='Kerkhoff Technologies Inc.',
    author_email='matt@kerkhofftech.ca',
    url="https://github.com/KerkhoffTechnologies/django-connectwise",
    include_package_data=True,
    test_suite='djconnectwise.tests.runtests.runtests',
    license='MIT',
    install_requires=[
        'requests',
        'django',
        'easy-thumbnails',
        'python-dateutil',
    ],
    zip_safe=False,  # Django likes to inspect apps for /migrations directories,
    # and can't if package is installed as a egg. zip_safe=False disables installation as an egg.
)
