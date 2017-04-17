# -*- coding: utf-8 -*-
#
# © 2017 Krux, A Salesforce Company
#

from __future__ import absolute_import

#########################
# Third Party Libraries #
#########################
import redis


class RedisInstance(object):
    """
    Presents a connection to a single redis instance
    """

    def __init__(
        self,
        parent,
        host='localhost',
        port=6379,
        db=0,
        password=None,
        timeout=None,

    ):
        self.parent = parent
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.connection = None
        self.timeout = None
        self.name = '%s:%s/%s' % (host, port, db)

    def connect(self):
        """
        Actually connect to the redis instance
        """
        log = self.parent.logger
        stats = self.parent.stats

        stats.incr('redis.instance.connect')

        if not self.connection:
            self.connection = redis.Redis(
                host=self.host,
                port=self.port,
                password=self.password,
                socket_timeout=self.timeout,
            )

        try:
            self.connection.ping()
            return self.connection

        except redis.RedisError, e:
            log.warning('Redis: Could not connect to %s: %s', self.name, e)
            stats.incr('redis.instance.error.connection')
            return None
