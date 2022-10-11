import os
import pytest
import logging
from typing import List

import psycopg2
from psycopg2_pool.base import Connection

from .utils import check_postgres_version

# Set by warm_up_database() the first time the dsn fixture is used
pg_version: int


def pytest_addoption(parser):
    parser.addoption(
        "--test-dsn",
        metavar="DSN",
        default=os.environ.get("PSYCOPG_TEST_DSN"),
        help=(
            "Connection string to run database tests requiring a connection"
            " [you can also use the PSYCOPG_TEST_DSN env var]."
        ),
    )


def pytest_report_header(config):
    dsn = config.getoption("--test-dsn")
    if dsn is None:
        return []

    try:
        with psycopg2.connect(dsn, connect_timeout=10) as conn:
            with conn.cursor() as cursor:
                cursor.execute("select version()")
                server_version = cursor.fetchall()[0][0]
    except Exception as ex:
        server_version = f"unknown ({ex})"

    return [
        f"Server version: {server_version}",
    ]


def pytest_collection_modifyitems(items):
    for item in items:
        for name in item.fixturenames:
            if name in ("pipeline", "apipeline"):
                item.add_marker(pytest.mark.pipeline)
                break


def pytest_configure(config):
    # register pg marker
    markers = [
        "pg(version_expr): run the test only with matching server version"
        " (e.g. '>= 10', '< 9.6')",
    ]
    for marker in markers:
        config.addinivalue_line("markers", marker)


@pytest.fixture(scope="session")
def session_dsn(request):
    """
    Return the dsn used to connect to the `--test-dsn` database (session-wide).
    """
    dsn = request.config.getoption("--test-dsn")
    if dsn is None:
        pytest.skip("skipping test as no --test-dsn")

    try:
        warm_up_database(dsn)
    except Exception:
        # This is a session fixture, so, in case of error, the exception would
        # be cached and nothing would run.
        # Let the caller fail instead.
        logging.exception("error warming up database")

    return dsn


@pytest.fixture
def dsn(session_dsn, request):
    """Return the dsn used to connect to the `--test-dsn` database."""
    check_connection_version(request.node)
    return session_dsn


@pytest.fixture
def conn(conn_cls, dsn, request, tracefile):
    """Return a `Connection` connected to the ``--test-dsn`` database."""
    check_connection_version(request.node)

    conn = psycopg2.connect(dsn, connection_factory=conn_cls)
    yield conn
    if not conn.closed:
        conn.close()


@pytest.fixture(scope="session")
def conn_cls(session_dsn):
    return Connection


def check_connection_version(node):
    try:
        pg_version
    except NameError:
        # First connection creation failed. Let the tests fail.
        pytest.fail("server version not available")

    for mark in node.iter_markers():
        if mark.name == "pg":
            assert len(mark.args) == 1
            msg = check_postgres_version(pg_version, mark.args[0])
            if msg:
                pytest.skip(msg)


def warm_up_database(dsn: str, __first_connection: List[bool] = [True]) -> None:
    """Connect to the database before returning a connection.

    In the CI sometimes, the first test fails with a timeout, probably because
    the server hasn't started yet. Absorb the delay before the test.
    """
    # Do it only once, even in case of failure, otherwise, in case of bad
    # configuration, with every test timing out, the entire test run would take
    # forever.
    if not __first_connection:
        return
    del __first_connection[:]

    global pg_version

    with psycopg2.connect(dsn, connect_timeout=10) as conn:
        with conn.cursor() as cursor:
            cursor.execute("select 1")

        pg_version = conn.info.server_version
