#!/usr/bin/env python3
"""
PostgreSQL database adapter for Python - Connection Pool
"""

# Copyright (C) 2020 The Psycopg Team

import re
from setuptools import setup

with open("psycopg2_pool/version.py") as f:
    data = f.read()
    m = re.search(r"""(?m)^__version__\s*=\s*['"]([^'"]+)['"]""", data)
    if not m:
        raise Exception(f"cannot find version in {f.name}")
    version = m.group(1)


setup(
    version=version,
)
