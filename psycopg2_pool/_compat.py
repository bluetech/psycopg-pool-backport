"""
compatibility functions for different Python versions
"""

# Copyright (C) 2021 The Psycopg Team

from enum import IntEnum
import sys

import psycopg2.extensions


if sys.version_info >= (3, 9):
    from collections import Counter, deque as Deque
else:
    from typing import Counter, Deque


class TransactionStatus(IntEnum):
    IDLE = psycopg2.extensions.TRANSACTION_STATUS_IDLE
    ACTIVE = psycopg2.extensions.TRANSACTION_STATUS_ACTIVE
    INTRANS = psycopg2.extensions.TRANSACTION_STATUS_INTRANS
    INERROR = psycopg2.extensions.TRANSACTION_STATUS_INERROR
    UNKNOWN = psycopg2.extensions.TRANSACTION_STATUS_UNKNOWN


__all__ = [
    "Counter",
    "Deque",
    "TransactionStatus",
]
