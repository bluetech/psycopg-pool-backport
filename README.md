# Psycopg2 connection pool - backport from Psycopg3

This package is an **unofficial** backport of psycopg3's connection pool to psycopg2.
The changes are meant to be minimal.
The full test suite and CI are also ported.

This package is useful for psycopg2 users who:

- have a need for a production-grade connection pool on psycopg2, and
- are unable to upgrade to psycopg3 as of yet

Backport changes:

- Backported the code from `psycopg` to `psycopg2`.
- Renamed PyPI package from `psycopg-pool` to `psycopg-pool-backport`.
- Renamed Python package from `psycopg_pool` to `psycopg2_pool`.
- Changed the logger name from `psycopg.pool` to `psycopg2_pool`.
- Removed async support.
- Removed `typing-extensions` dependency.

See the original [`psycopg-pool` documentation](https://www.psycopg.org/psycopg3/docs/advanced/pool.html) for usage details.
See the [psycopg repo](https://github.com/psycopg/psycopg/tree/master/psycopg_pool) for the upstream code.

You can install this package using:

    pip install psycopg-pool-backport

Copyright (C) 2020 The Psycopg Team
