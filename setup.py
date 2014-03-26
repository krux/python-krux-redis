# -*- coding: utf-8 -*-
#
# © 2014 Krux Digital, Inc.
#
"""
Package setup for krux-redis
"""
######################
# Standard Libraries #
######################
from __future__ import absolute_import
from setuptools import setup, find_packages

import os


# We use the version to construct the DOWNLOAD_URL.
VERSION      = '0.0.3'

# URL to the repository on Github.
REPO_URL     = 'https://github.com/krux/python-krux-redis'
# Github will generate a tarball as long as you tag your releases, so don't
# forget to tag!
DOWNLOAD_URL = ''.join((REPO_URL, '/tarball/release/', VERSION))


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
    install_requires = [
        'redis',
        'krux-stdlib',
    ],
)
