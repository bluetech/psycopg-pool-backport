def pytest_configure(config):
    # register libpq marker
    config.addinivalue_line(
        "markers",
        "crdb(version_expr, reason=detail): run/skip the test with matching CockroachDB"
        " (e.g. '>= 21.2.10', '< 22.1', 'skip < 22')",
    )
    config.addinivalue_line(
        "markers",
        "crdb_skip(reason): skip the test for known CockroachDB reasons",
    )
