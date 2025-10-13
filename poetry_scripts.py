import sys

import pytest


def test():
    """
    Run the project's test suite in the "tests" directory and exit the process with pytest's returned status code.
    """
    sys.exit(pytest.main(["tests/"]))


def test_fast():
    """
    Run tests in the `tests/` directory with pytest's `addopts` ini option overridden to an empty value, then exit the process with pytest's return code.
    """
    sys.exit(pytest.main(["--override-ini=addopts=''", "tests/"]))


def test_cov():
    """
    Run the test suite with coverage measurement for the `app` package and exit with pytest's status code.
    
    Runs pytest for the `tests/` directory with coverage enabled for the `app` package, produces a terminal-missing coverage report and an HTML coverage report, and terminates the process using pytest's exit code.
    """
    sys.exit(pytest.main(["--cov=app", "--cov-report=term-missing", "--cov-report=html", "tests/"]))