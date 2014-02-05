#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='pystash',
    version='0.1',
    description='A proxy for python logging UDP/TCP to logstash/redis',
    long_description=readme + '\n\n' + history,
    author='Sebastien Estienne',
    author_email='sebastien.estienne@gmail.com',
    url='https://github.com/sebest/pystash',
    packages=[
        'pystash',
    ],
    package_dir={'pystash': 'pystash'},
    include_package_data=True,
    install_requires=[
        'redis',
        'gevent',
    ],
    license="BSD",
    zip_safe=False,
    keywords='pystash',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    test_suite='tests',
    entry_points = {
        'console_scripts': [
            'pystash = pystash.cli:main',
        ]
    }
)
