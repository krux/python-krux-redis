# -*- coding: utf-8 -*-
#
# © 2017 Krux, A Salesforce Company
#
from __future__ import absolute_import
from setuptools import setup, find_packages
import os
import sys
from krux_redis import __version__


# subprocess32 is required by krux-stdlib, but breaks builds on
# python3, so we append it to the requirements and do *not* specify
# the version in requirements.pip.
REQUIREMENTS = ['krux-stdlib']
if os.name == 'posix' and sys.version_info[0] < 3:
    # For Python 2.*, install the backported subprocess
    REQUIREMENTS.append('subprocess32')


setup(
    name='krux-redis',
    version=__version__,
    author='Jos Boumans',
    author_email='jos@krux.com',
    maintainer='Paul Lathrop',
    maintainer_email='plathrop@salesforce.com',
    description='Standard libraries and tools for Sentinel clusters at Krux.',
    long_description="""
    Standard libraries and tools for interacting with Redis Sentinel
    clusters at Krux.
    """,
    url='https://github.com/krux/python-krux-redis',
    license='All Rights Reserved.',
    packages=find_packages(),
    install_requires=REQUIREMENTS,
)
