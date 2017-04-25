# -*- coding: utf-8 -*-
#
# © 2017 Krux, A Salesforce Company
#

from __future__ import absolute_import

from redis.sentinel import ConnectionError, Sentinel

from krux.cli import Application
from krux_redis.cli import add_sentinel_cli_arguments


SEPARATOR = ':'
SOCKET_TIMEOUT = 0.1


def hostport_from_string(spec):
    """
    Given SPEC, a string specifying a HOST:PORT pair, return a tuple
    of (HOST, PORT).
    """
    return tuple(spec.split(SEPARATOR))


def hostports_from_args(args):
    """
    Given a Namespace object (parsed CLI options), return a list of
    (HOST, PORT) pairs specified by the Namespace.
    """
    return [hostport_from_string(s) for s in getattr(args, 'sentinel', [])]


class TestApplication(Application):
    def __init__(self):
        # Call to the superclass to bootstrap.
        super(TestApplication, self).__init__(name='krux-redis-sentinel')

        self.logger.debug('Parsing sentinels from args: %r', self.args.sentinel)
        sentinels = hostports_from_args(self.args)
        self.logger.debug('Parsed sentinel host, port pairs: %r', sentinels)

        self.logger.debug('Initializing Sentinel instance...')
        self.sentinel = Sentinel(sentinels, socket_timeout=SOCKET_TIMEOUT)
        self.logger.debug('Initialized Sentinel instance: %r', self.sentinel)

    def add_cli_arguments(self, parser):
        add_sentinel_cli_arguments(parser)

    def run(self):
        master = self.sentinel.master_for(self.name)
        slave = self.sentinel.slave_for(self.name)

        try:
            self.logger.info('Ping master: %s', master.ping())
        except ConnectionError as err:
            self.logger.warning('Could not connect to master!')
            self.logger.error(err)

        try:
            self.logger.info('Ping slave: %s', slave.ping())
        except ConnectionError as err:
            self.logger.warning('Could not connect to slave!')
            self.logger.error(err)


def main():
    TestApplication().run()


# Run the application stand alone
if __name__ == '__main__':
    main()
