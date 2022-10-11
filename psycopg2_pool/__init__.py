"""
psycopg connection pool package
"""

# Copyright (C) 2021 The Psycopg Team

from .pool import ConnectionPool
from .null_pool import NullConnectionPool
from .errors import PoolClosed, PoolTimeout, TooManyRequests
from .version import __version__ as __version__  # noqa: F401

__all__ = [
    "ConnectionPool",
    "NullConnectionPool",
    "PoolClosed",
    "PoolTimeout",
    "TooManyRequests",
]
