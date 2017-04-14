# -*- coding: utf-8 -*-
#
# © 2017 Krux, A Salesforce Company
#

from __future__ import absolute_import

from krux.cli import get_group


DEFAULT_TIMEOUT = 0.5   # in seconds


# Designed to be called from krux.cli, or programs inheriting from it
def add_redis_cli_arguments(parser):

    group = get_group(parser, 'redis')

    group.add_argument(
        '--redis-master',
        default='redis://localhost:6379/0',
        help='Redis master url (default: %(default)s)',
    )

    group.add_argument(
        '--redis-slave',
        action='append',
        default=[],
        help='Redis slave urls (default: %(default)s)'
    )

    group.add_argument(
        '--redis-timeout',
        default=DEFAULT_TIMEOUT,
        help='Timeout for redis calls, in seconds (default: %(default)s)'
    )
