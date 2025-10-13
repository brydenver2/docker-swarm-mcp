import sys

import pytest


def test():
    """
    Run the project's test suite in the "tests" directory and exit the process with pytest's returned status code.
    """
    sys.exit(pytest.main(["tests/"]))


def test_fast() -> int:
    """
    Run tests in the `tests/` directory with pytest's `addopts` ini option overridden to an empty value.

    Returns:
        int: Pytest's exit code.
    """
    return int(pytest.main(["--override-ini=addopts=''", "tests/"]))


def test_cov(package: str = "app", test_path: str = "tests/") -> int:
    """
    Run the test suite with coverage measurement for the given package.

    Args:
        package: Package name or dotted path to measure for coverage (default: "app").
        test_path: Directory or file path containing tests to execute (default: "tests/").

    Returns:
        int: Pytest's exit code.
    """
    return int(
        pytest.main(
            [
                f"--cov={package}",
                "--cov-report=term-missing",
                "--cov-report=html",
                test_path,
            ]
        )
    )
