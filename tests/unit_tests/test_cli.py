# -*- coding: utf-8 -*-
#
# © 2017 Krux, A Salesforce Company
#

from __future__ import absolute_import
from argparse import ArgumentParser

from nose.tools import assert_true

from krux_redis.cli import (
    DEFAULT_REDIS_MASTER,
    DEFAULT_REDIS_TIMEOUT,
    DEFAULT_SENTINEL_HOSTPORT,
    add_redis_cli_arguments,
    add_sentinel_cli_arguments,
)


REDIS_MASTER_DEST = 'redis_master'
REDIS_SLAVE_DEST = 'redis_slave'
REDIS_TIMEOUT_DEST = 'redis_timeout'
SENTINEL_DEST = 'sentinel'
SENTINEL_TIMEOUT_DEST = 'sentinel_timeout'


def test_add_redis_cli_args():
    """
    add_redis_cli_arguments() correctly adds arguments to the parser.
    """
    parser = ArgumentParser()
    add_redis_cli_arguments(parser)
    options = parser.parse_args()

    assert_true(hasattr(options, REDIS_MASTER_DEST))
    assert_true(getattr(options, REDIS_MASTER_DEST) == DEFAULT_REDIS_MASTER)

    assert_true(hasattr(options, REDIS_SLAVE_DEST))
    assert_true(getattr(options, REDIS_SLAVE_DEST) == [])

    assert_true(hasattr(options, REDIS_TIMEOUT_DEST))
    assert_true(getattr(options, REDIS_TIMEOUT_DEST) == DEFAULT_REDIS_TIMEOUT)


def test_add_sentinel_cli_args():
    """
    add_sentinel_cli_arguments() correctly adds arguments to the parser.
    """
    parser = ArgumentParser()
    add_sentinel_cli_arguments(parser)
    options = parser.parse_args([])

    assert_true(hasattr(options, SENTINEL_DEST))
    assert_true(getattr(options, SENTINEL_DEST) == [DEFAULT_SENTINEL_HOSTPORT])

    assert_true(hasattr(options, SENTINEL_TIMEOUT_DEST))
    assert_true(
        getattr(options, SENTINEL_TIMEOUT_DEST) == DEFAULT_REDIS_TIMEOUT
    )
