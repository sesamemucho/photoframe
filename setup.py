#!/usr/bin/env python

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
doclink = """
Documentation
-------------

The full documentation is at http://photoframe.rtfd.org."""
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='photoframe',
    version='0.1.0',
    description='Code for photo frame Raspberry Pi project',
    long_description=readme + '\n\n' + doclink + '\n\n' + history,
    author='Bob Forgey',
    author_email='rforgey@grumpydogconsulting.com',
    url='https://github.com/sesamemucho/photoframe',
    packages=[
        'photoframe',
    ],
    scripts=['bin/photoframe'],
    package_dir={'photoframe': 'photoframe'},
    include_package_data=True,
    install_requires=[
    ],
    license='MIT',
    zip_safe=False,
    keywords='photoframe',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
