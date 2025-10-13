import sys

import pytest


def test():
    sys.exit(pytest.main(["tests/"]))


def test_fast():
    sys.exit(pytest.main(["--override-ini=addopts=''", "tests/"]))


def test_cov():
    sys.exit(pytest.main(["--cov=app", "--cov-report=term-missing", "--cov-report=html", "tests/"]))
