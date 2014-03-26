######################
# Standard Libraries #
######################
from __future__ import absolute_import

from urlparse import urlparse
from pprint   import pprint

import random

#########################
# Third Party Libraries #
#########################
import redis

from krux.logging     import get_logger, LEVELS
from krux.stats       import get_stats
from krux.cli         import get_parser, get_group, Application

#########################
# Constants
#########################

DEFAULT_HOST    = 'localhost'
DEFAULT_PORT    = 6379
DEFAULT_DB      = 0
DEFAULT_TIMEOUT = 0.5   # in seconds

### Designed to be called from krux.cli, or programs inheriting from it
def add_redis_cli_arguments(parser):

    group = get_group(parser, 'redis')

    group.add_argument(
        '--redis-master',
        default = 'redis://localhost:6379/0',
        help    = 'Redis master url (default: %(default)s)',
    )

    group.add_argument(
        '--redis-slave',
        action  = 'append',
        default = [ ],
        help    = 'Redis slave urls (default: %(default)s)'
    )

    group.add_argument(
        '--redis-timeout',
        default = DEFAULT_TIMEOUT,
        help    = 'Timeout for redis calls, in seconds (default: %(default)s)'
    )

class Redis(object):

    def __init__(self, logger = None, stats = None, parser = None):
        self.master = None
        self.slaves = [ ]

        self.name   = 'krux-redis'
        self.logger = logger or get_logger(self.name)
        self.stats  = stats  or get_stats( prefix      = self.name)
        self.parser = parser or get_parser(description = self.name)

        ### in case we got some of the information via the CLI
        self.args       = self.parser.parse_args()


    def set_master(self, instance, *args, **kwargs):
        self.master = self.___create_instance(instance)

    def add_slave(self, instance, *args, **kwargs):
        self.slaves.append( self.___create_instance(instance) )

    def ___create_instance( self, instance, *args, **kwargs ):
        """
        If you pass a string, we'll parse it like it's a URI.
        Otherwise, it's assumed to implement a RedisInstance interface.
        """

        if isinstance(instance, str):
            return self.from_url(instance, *args, **kwargs)
        else:
            return instance


    def from_url(self, url, *args, **kwargs):
        """
        Create a redis connection from a URL, like: redis://pass@localhost:6379/0
        """

        parsed = urlparse(url)

        ### this will hold /0, or something like that
        db = parsed.path.lstrip('/')
        db = int(db) if len(db) else DEFAULT_DB

        return RedisInstance(
            host        = parsed.hostname or DEFAULT_HOST,
            port        = parsed.port     or DEFAULT_PORT,
            db          = db,
            ### it's usually just password@redishost, so then it's
            ### pasred into the username attribute.
            password    = parsed.password or parsed.username,
            parent      = self,
            **kwargs
        )

    def from_cli(self):
        args = self.args

        ### add the master
        self.set_master( args.redis_master, timeout = args.redis_timeout )

        ### add the slave
        for slave in args.redis_slave:
            self.add_slave( slave, timeout = args.redis_timeout )

    def get_master(self):
        return self.master.connect()

    def get_slave(self):
        log     = self.logger
        stats   = self.stats
        slaves  = self.slaves

        ### randomize the list so we sorta-round-robin. Note that this
        ### gets shuffled in place, so that's why we use a copy.
        random.shuffle(slaves)

        with stats.timer('redis.get_slave'):
            for slave in slaves:

                log.debug('Trying slave: %s', slave.name)
                conn = slave.connect()

                ### did we get a working connection?
                if conn:
                    log.debug('Redis: Found connected slave: %s', slave.name)
                    return conn

            ### got here? No slaves are working, so use the master
            log.debug('Redis: No slaves found - returning master')
            stats.incr('redis.error.no_slave')
            return self.get_master()


class RedisInstance(object):
    """
    Presents a connection to a single redis instance
    """

    def __init__(
        self,
        parent,
        host        = 'localhost',
        port        = 6379,
        db          = 0,
        password    = None,
        timeout     = None,

    ):
        self.parent     = parent
        self.host       = host
        self.port       = port
        self.db         = db
        self.password   = password
        self.connection = None
        self.timeout    = None
        self.name       = '%s:%s/%s' % (host, port, db)

    def connect(self):
        """
        Actually connect to the redis instance
        """
        log     = self.parent.logger
        stats   = self.parent.stats

        stats.incr('redis.instance.connect')

        if not self.connection:
            self.connection = redis.Redis(
                host            = self.host,
                port            = self.port,
                password        = self.password,
                socket_timeout  = self.timeout,
            )

        try:
            self.connection.ping()
            return self.connection

        except redis.RedisError, e:
            log.warning('Redis: Could not connect to %s: %s', self.name, e)
            stats.incr('redis.instance.error.connection')
            return None

class TestApplication(Application):

    def __init__(self):
        ### Call to the superclass to bootstrap.
        super(TestApplication, self).__init__(name = 'krux-redis')

        ### get all the redis configuration from the CLI
        self.redis  = Redis(
                        parser = self.parser,
                        logger = self.logger,
                        stats  = self.stats,
                      )
        self.redis.from_cli()

    def add_cli_arguments(self, parser):

        ### we use redis, but via CLI arguments.
        add_redis_cli_arguments(parser)

def main():
    app     = TestApplication()
    log     = app.logger
    master  = app.redis.get_master()
    slave   = app.redis.get_slave()

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

### Run the application stand alone
if __name__ == '__main__':
    main()

