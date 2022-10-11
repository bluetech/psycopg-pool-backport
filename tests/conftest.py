from typing import List

import pytest

pytest_plugins = (
    "tests.fix_db",
    "tests.fix_mypy",
    "tests.fix_proxy",
    "tests.fix_crdb",
    "tests.pool.fix_pool",
)


def pytest_configure(config):
    markers = [
        "slow: this test is kinda slow (skip with -m 'not slow')",
        "flakey(reason): this test may fail unpredictably')",
        "timing: the test is timing based and can fail on cheese hardware",
    ]

    for marker in markers:
        config.addinivalue_line("markers", marker)


def pytest_addoption(parser):
    parser.addoption(
        "--no-collect-ok",
        action="store_true",
        help=(
            "If no test collected, exit with 0 instead of 5 (useful with --lfnf=none)."
        ),
    )

    parser.addoption(
        "--allow-fail",
        metavar="NUM",
        type=int,
        default=0,
        help="Tolerate up to NUM failures. Use carefully.",
    )


def pytest_sessionstart(session):
    # Detect if there was a segfault in the previous run.
    #
    # In case of segfault, pytest doesn't get a chance to write failed tests
    # in the cache. As a consequence, tox retries would find no test failed and
    # assume that all tests passed in the previous run, making the whole test pass.
    #
    # Note: The cache is in .pytest_cache/
    cache = session.config.cache
    if cache.get("segfault", False):
        session.warn(Warning("Previous run resulted in segfault! Not running any test"))
        raise session.Failed
    cache.set("segfault", True)


allow_fail_messages: List[str] = []


def pytest_sessionfinish(session, exitstatus):
    # Mark the test run successful (in the sense -weak- that we didn't segfault).
    session.config.cache.set("segfault", False)

    no_collect_ok = session.config.getoption("--no-collect-ok")
    if exitstatus == pytest.ExitCode.NO_TESTS_COLLECTED and no_collect_ok:
        session.exitstatus = pytest.ExitCode.OK

    allow_fail = session.config.getoption("--allow-fail")
    if exitstatus == pytest.ExitCode.TESTS_FAILED:
        if session.testsfailed <= allow_fail:
            allow_fail_messages.append(f"Tests failed: {session.testsfailed}")
            allow_fail_messages.append(f"Failures allowed: {allow_fail}")
            session.exitstatus = pytest.ExitCode.OK


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    if allow_fail_messages:
        terminalreporter.section("failed tests ignored")
        for msg in allow_fail_messages:
            terminalreporter.line(msg)
