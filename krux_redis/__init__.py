# -*- coding: utf-8 -*-
#
# © 2017 Krux, A Salesforce Company
#

from __future__ import absolute_import


# PEP-8 says module-level "dunders" (double-underscore vars) like this
# one should go before imports (but after the absolute_import line).
__version__ = '0.1.0'

# @plathrop 2017.04.14: For API backwards-compatibility we import
# things which were refactored into separate modules and provide some
# module-level constants that were present in previous versions. These
# are deprecated and should be removed in a future version.
#
# Since these are intended, we supress flake8 checks via the noqa
# tags; F401 is the unused import check.
from krux_redis.cli import add_redis_cli_arguments, DEFAULT_REDIS_TIMEOUT # noqa:F401
from krux_redis.redis_instance import RedisInstance # noqa:F401


# Deprecated, see comment above
DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 6379
DEFAULT_DB = 0
