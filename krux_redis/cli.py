# -*- coding: utf-8 -*-
#
# © 2017 Krux, A Salesforce Company
#

from __future__ import absolute_import

from krux.cli import get_group


DEFAULT_REDIS_MASTER = 'redis://localhost:6379/0'
DEFAULT_REDIS_TIMEOUT = 0.5   # in seconds
DEFAULT_SENTINEL_HOSTPORT = '127.0.0.1:26379'
GROUP_NAME = 'redis'


# Designed to be called from krux.cli, or programs inheriting from it
#
# TODO: Potentially refactor this. See: https://git.io/vSFYS
def add_redis_cli_arguments(parser):

    group = get_group(parser, GROUP_NAME)

    group.add_argument(
        '--redis-master',
        default=DEFAULT_REDIS_MASTER,
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
        default=DEFAULT_REDIS_TIMEOUT,
        help='Timeout for redis calls, in seconds (default: %(default)s)'
    )


def add_sentinel_cli_arguments(parser):

    group = get_group(parser, GROUP_NAME)

    group.add_argument(
        '--sentinel',
        default=[DEFAULT_SENTINEL_HOSTPORT],
        nargs='*',
        help='HOST:PORT pairs of Redis Sentinel instances to contact. '
        'default: %(default)s',
    )

    group.add_argument(
        '--sentinel-timeout',
        default=DEFAULT_REDIS_TIMEOUT,
        help='Timeout for Redis Sentinel calls, in seconds '
        '(default: %(default)s)',
    )
