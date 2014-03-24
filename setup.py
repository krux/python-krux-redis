# -*- coding: utf-8 -*-
#
# © 2013 Krux Digital, Inc.
#
"""
Package setup for krux-redis
"""
######################
# Standard Libraries #
######################
from __future__ import absolute_import
from setuptools import setup, find_packages
from pip.req    import parse_requirements

import os


# We use the version to construct the DOWNLOAD_URL.
VERSION      = '0.0.1'

# URL to the repository on Github.
REPO_URL     = 'https://github.com/krux/python-krux-redis'
# Github will generate a tarball as long as you tag your releases, so don't
# forget to tag!
DOWNLOAD_URL = ''.join((REPO_URL, '/tarball/release/', VERSION))

# We want to install all the dependencies of the library as well, but we
# don't want to duplicate the dependencies both here and in
# requirements.pip. Instead we parse requirements.pip to pull in our
# dependencies.
BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
REQUIREMENTS = os.path.join(BASE_DIR, 'requirements.pip')

# A requirement file can contain comments (#) and can include some other
# files (--requirement or -r), so we need to use pip's parser to get the
# final list of dependencies.
ALL_DEPENDENCIES = set([unicode(package.req)
                    for package in parse_requirements(REQUIREMENTS)])

setup(
    name             = 'krux-redis',
    version          = VERSION,
    author           = 'Jos Boumans',
    author_email     = 'jos@krux.com',
    description      = 'Library to wrap redsi.py for writers & multiple readers',
    url              = REPO_URL,
    download_url     = DOWNLOAD_URL,
    license          = 'All Rights Reserved.',
    packages         = find_packages(),
    install_requires = ALL_DEPENDENCIES,
)
