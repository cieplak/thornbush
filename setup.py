#!/usr/bin/env python

from setuptools import setup, find_packages


requirements = [
    'sqlalchemy',
    'Flask',
    'pytz',
    'hashlib',
    'click',
    'psycopg2',
]


setup(
    name='thornbush',
    version='0.0.1',
    url='https://www.github.com/cieplak/thornbush',
    author='patrick cieplak',
    author_email='patrick.cieplak@gmail.com',
    description='Simple REST API for threaded comments',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=requirements,
    tests_require=['pytest', 'mock>=0.8'],
)
