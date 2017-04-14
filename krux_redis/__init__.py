# -*- coding: utf-8 -*-
#
# © 2017 Krux, A Salesforce Company
#

from __future__ import absolute_import


# PEP-8 says module-level "dunders" (double-underscore vars) like this
# one should go before imports (but after the absolute_import line).
__version__ = '0.1.0'

############################
# Krux Standard Libararies #
############################
from krux.cli import Application
from krux_redis.client import Redis


# @plathrop 2017.04.14: For API backwards-compatibility we import
# things which were refactored into separate modules and provide some
# module-level constants that were present in previous versions. These
# are deprecated and should be removed in a future version.
#
# Since these are intended, we supress flake8 checks via the noqa
# tags; F401 is the unused import check.
from krux_redis.cli import add_redis_cli_arguments, DEFAULT_TIMEOUT # noqa:F401
from krux_redis.client import RedisInstance # noqa:F401


# Deprecated, see comment above
DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 6379
DEFAULT_DB = 0


class TestApplication(Application):

    def __init__(self):
        # Call to the superclass to bootstrap.
        super(TestApplication, self).__init__(name='krux-redis')

        # get all the redis configuration from the CLI
        self.redis = Redis(
            parser=self.parser,
            logger=self.logger,
            stats=self.stats,
        )
        self.redis.from_cli()

    def add_cli_arguments(self, parser):

        # we use redis, but via CLI arguments.
        add_redis_cli_arguments(parser)


def main():
    app = TestApplication()
    log = app.logger
    master = app.redis.get_master()
    slave = app.redis.get_slave()

    if master:
        log.info('Connected to master %s', master)
        log.info('Ping master: %s', master.ping())
    else:
        log.warning('Could not connect to master')

    if slave:
        log.info('Connected to master %s', slave)
        log.info('Ping slave: %s', slave.ping())
    else:
        log.warning('Could not connect to slave')


# Run the application stand alone
if __name__ == '__main__':
    main()
