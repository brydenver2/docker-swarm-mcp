================
CODE SNIPPETS
================
TITLE: Verify pytest installation and version
DESCRIPTION: This command checks the installed version of pytest to confirm successful installation and readiness for use. It outputs the pytest version along with supporting Python and pluggy versions.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/getting-started.rst

LANGUAGE: bash
CODE:
```
$ pytest --version
pytest 8.4.2
```

--------------------------------

TITLE: List Available Pytest Fixtures
DESCRIPTION: This command-line example shows how to use `pytest --fixtures` to display a list of all available fixtures, including both built-in ones and any custom fixtures defined in the project. Adding the `-v` option will also reveal fixtures with leading underscores that are typically hidden.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/getting-started.rst

LANGUAGE: bash
CODE:
```
pytest --fixtures   # shows builtin and custom fixtures
```

--------------------------------

TITLE: Set Up Pytest Development Environment with Virtual Environment
DESCRIPTION: These commands guide the user through creating a virtual environment, activating it (for both Linux and Windows), and installing Pytest in editable mode with development dependencies. This allows for direct local testing and development.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/CONTRIBUTING.rst

LANGUAGE: bash
CODE:
```
$ python3 -m venv .venv
$ source .venv/bin/activate  # Linux
$ .venv/Scripts/activate.bat  # Windows
$ pip install -e ".[dev]"
```

--------------------------------

TITLE: Define a basic pytest function and test
DESCRIPTION: This Python code defines a simple function `func` and a test function `test_answer` that uses an `assert` statement to verify the function's output. This `test_sample.py` file demonstrates the fundamental structure of a pytest test.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/getting-started.rst

LANGUAGE: python
CODE:
```
# content of test_sample.py
def func(x):
    return x + 1


def test_answer():
    assert func(3) == 5
```

--------------------------------

TITLE: Execute a basic pytest test and observe failure
DESCRIPTION: This command runs pytest on the `test_sample.py` file, demonstrating how pytest discovers and executes tests. The output illustrates a test session, test collection, and an `AssertionError` for `test_answer` because `func(3)` (which is 4) does not equal 5.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/getting-started.rst

LANGUAGE: pytest
CODE:
```
$ pytest
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 1 item

test_sample.py F                                                     [100%]

================================= FAILURES =================================
_______________________________ test_answer ________________________________

    def test_answer():
>       assert func(3) == 5
E       assert 4 == 5
E        +  where 4 = func(3)

test_sample.py:6: AssertionError
========================= short test summary info ==========================
FAILED test_sample.py::test_answer - assert 4 == 5
============================ 1 failed in 0.12s =============================
```

--------------------------------

TITLE: Run pytest with quiet mode for exception test
DESCRIPTION: This command executes the `test_sysexit.py` file using pytest with the quiet mode (`-q`) flag, which provides a concise output. The result shows that the test for `SystemExit` passes successfully, indicating the exception was caught as expected.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/getting-started.rst

LANGUAGE: pytest
CODE:
```
$ pytest -q test_sysexit.py
.                                                                    [100%]
1 passed in 0.12s
```

--------------------------------

TITLE: Run Pytest with Incremental Test Example
DESCRIPTION: This command shows how to execute the `test_step.py` tests with pytest. The output demonstrates that `test_modification` fails, and `test_deletion` is subsequently marked as an expected failure (XFAIL) due to the incremental testing setup, confirming the functionality.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst

LANGUAGE: bash
CODE:
```
$ pytest -rx
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 4 items

test_step.py .Fx.                                                    [100%]

================================= FAILURES =================================
____________________ TestUserHandling.test_modification ____________________

self = <test_step.TestUserHandling object at 0xdeadbeef0001>

    def test_modification(self):
>       assert 0
E       assert 0

test_step.py:11: AssertionError
========================= short test summary info ==========================
XFAIL test_step.py::TestUserHandling::test_deletion - previous test failed (test_modification)
================== 1 failed, 2 passed, 1 xfailed in 0.12s ==================
```

--------------------------------

TITLE: Decorate pytest funcarg at module level for specialized setup (Python)
DESCRIPTION: This Python code shows how to extend an existing funcarg (like `accept`) at the module level. The `pytest_funcarg__accept` function calls the next factory to get the base `accept` fixture, then modifies its state (e.g., creating a 'special' directory in `tmpdir`) before returning it. This allows for module-specific test setups while reusing the core fixture logic.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/attic.rst

LANGUAGE: python
CODE:
```
def pytest_funcarg__accept(request):
    # call the next factory (living in our conftest.py)
    arg = request.getfuncargvalue("accept")
    # create a special layout in our tempdir
    arg.tmpdir.mkdir("special")
    return arg


class TestSpecialAcceptance:
    def test_sometest(self, accept):
        assert accept.tmpdir.join("special").check()
```

--------------------------------

TITLE: Pytest Module with Setup and Call Phase Failures
DESCRIPTION: This Python module contains tests designed to fail at different stages: `other` fixture fails during setup, leading to `test_setup_fails` error. `test_call_fails` fails during its execution phase, and `test_fail2` is a standard failing test. These tests demonstrate the functionality of the `conftest.py` plugin for reporting test outcomes in fixtures.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst

LANGUAGE: python
CODE:
```
    # content of test_module.py

    import pytest


    @pytest.fixture
    def other():
        assert 0


    def test_setup_fails(something, other):
        pass


    def test_call_fails(something):
        assert 0


    def test_fail2():
        assert 0
```

--------------------------------

TITLE: Implement pytest_runtest_setup hook in conftest.py for directory-specific tests
DESCRIPTION: This example demonstrates how to implement the `pytest_runtest_setup` hook within a `conftest.py` file to execute setup logic specifically for tests within a particular directory (`a/`). It showcases the `conftest.py` defining the hook, a test file in the same directory, and another test file outside it, highlighting the local scope of the hook.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/writing_plugins.rst

LANGUAGE: python
CODE:
```
# a/conftest.py
def pytest_runtest_setup(item):
    # called for running each test in 'a' directory
    print("setting up", item)

# a/test_sub.py
def test_sub():
    pass

# test_flat.py
def test_flat():
    pass
```

--------------------------------

TITLE: Assert a SystemExit exception using pytest.raises
DESCRIPTION: This Python code demonstrates how to use `pytest.raises` as a context manager to assert that a specific exception, `SystemExit` in this example, is raised by a function `f`. This feature is essential for robust testing of error handling mechanisms.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/getting-started.rst

LANGUAGE: python
CODE:
```
# content of test_sysexit.py
import pytest


def f():
    raise SystemExit(1)


def test_mytest():
    with pytest.raises(SystemExit):
        f()
```

--------------------------------

TITLE: Install Project in Development Mode with pip
DESCRIPTION: This snippet provides commands to navigate to a project's root directory and install it in editable/development mode using `pip install -e .`. This setup allows developers to make code changes and have them immediately reflected when running tests, avoiding frequent reinstalls.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/existingtestsuite.rst

LANGUAGE: bash
CODE:
```
cd <repository>
pip install -e .  # Environment dependent alternatives include
                  # 'python setup.py develop' and 'conda develop'
```

--------------------------------

TITLE: Install and Run pytest
DESCRIPTION: Instructions for installing the latest version of pytest using pip and then executing it from the command line. This ensures users have the most up-to-date testing framework and can immediately begin using its features.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/__wiki__/pytest-3.0-checklist.md

LANGUAGE: shell
CODE:
```
pip install -U pytest
```

LANGUAGE: shell
CODE:
```
pytest
```

--------------------------------

TITLE: Define Interdependent pytest Fixtures for Modular Application Setup
DESCRIPTION: This Python example showcases how fixtures can depend on other fixtures, promoting a modular design. An `App` class is defined, and an `app` fixture is created that consumes a previously defined `smtp_connection` fixture. The `test_smtp_connection_exists` function then asserts the presence of the connection within the `App` instance, demonstrating how to build complex setup logic by composing fixtures.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst

LANGUAGE: python
CODE:
```
# content of test_appsetup.py

import pytest


class App:
    def __init__(self, smtp_connection):
        self.smtp_connection = smtp_connection


@pytest.fixture(scope="module")
def app(smtp_connection):
    return App(smtp_connection)


def test_smtp_connection_exists(app):
    assert app.smtp_connection
```

--------------------------------

TITLE: Install argcomplete for pytest bash completion
DESCRIPTION: This command uses `pip` with `sudo` to install the `argcomplete` package globally, specifying a minimum version requirement (0.5.7) necessary for `pytest`'s bash completion functionality.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/bash-completion.rst

LANGUAGE: bash
CODE:
```
sudo pip install 'argcomplete>=0.5.7'
```

--------------------------------

TITLE: Utilize Pytest tmp_path Fixture for Temporary Directories
DESCRIPTION: This example demonstrates how to use the built-in `tmp_path` fixture to request a unique temporary directory for a test. By including `tmp_path` in the test function signature, pytest automatically creates a distinct temporary directory (as a `pathlib.Path` object) before the test runs, ensuring a clean environment for file-based tests.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/getting-started.rst

LANGUAGE: python
CODE:
```
# content of test_tmp_path.py
def test_needsfiles(tmp_path):
    print(tmp_path)
    assert 0
```

LANGUAGE: pytest
CODE:
```
$ pytest -q test_tmp_path.py
F                                                                    [100%]
================================= FAILURES =================================
_____________________________ test_needsfiles ______________________________

tmp_path = PosixPath('PYTEST_TMPDIR/test_needsfiles0')

    def test_needsfiles(tmp_path):
        print(tmp_path)
>       assert 0
E       assert 0

test_tmp_path.py:3: AssertionError
--------------------------- Captured stdout call ---------------------------
PYTEST_TMPDIR/test_needsfiles0
========================= short test summary info ==========================
FAILED test_tmp_path.py::test_needsfiles - assert 0
1 failed in 0.12s
```

--------------------------------

TITLE: Install and Configure pre-commit Hooks for Code Quality
DESCRIPTION: This snippet installs the `pre-commit` tool for the current user and then installs its Git hooks into the local repository. This ensures that style-guides and code checks are automatically run before each commit, maintaining code consistency.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/CONTRIBUTING.rst

LANGUAGE: shell
CODE:
```
$ pip install --user pre-commit
$ pre-commit install
```

--------------------------------

TITLE: Run Pytest Tests Using --pyargs Option
DESCRIPTION: This bash command demonstrates how to execute tests that are part of an application package using pytest's `--pyargs` option. pytest will automatically locate the installed `mypkg` and collect all associated tests from its structure, making it convenient for inlined test setups.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/explanation/goodpractices.rst

LANGUAGE: bash
CODE:
```
pytest --pyargs mypkg
```

--------------------------------

TITLE: Execute class-based pytest tests and analyze failure
DESCRIPTION: This command runs the tests defined in `test_class.py` using pytest in quiet mode. The output demonstrates that `test_one` passes while `test_two` fails due to an `AssertionError`, showcasing pytest's detailed reporting for failures within class methods.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/getting-started.rst

LANGUAGE: pytest
CODE:
```
$ pytest -q test_class.py
.F                                                                   [100%]
================================= FAILURES =================================
____________________________ TestClass.test_two ____________________________

self = <test_class.TestClass object at 0xdeadbeef0001>

    def test_two(self):
        x = "hello"
>       assert hasattr(x, "check")
E       AssertionError: assert False
E        +  where False = hasattr('hello', 'check')

test_class.py:8: AssertionError
========================= short test summary info ==========================
FAILED test_class.py::TestClass::test_two - AssertionError: assert False
1 failed, 1 passed in 0.12s
```

--------------------------------

TITLE: Install or Upgrade pytest using pip or easy_install
DESCRIPTION: These commands demonstrate how to install or upgrade the pytest testing framework in a Python environment. 'pip' is the standard package installer, while 'easy_install' is an older alternative. The '-U' flag ensures that any existing installation is updated to the latest available version.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-2.3.4.rst

LANGUAGE: shell
CODE:
```
pip install -U pytest
```

LANGUAGE: shell
CODE:
```
easy_install -U pytest
```

--------------------------------

TITLE: Python Optimized Module for API Comparison (opt1)
DESCRIPTION: The `opt1.py` file presents an alternative implementation of `func1()` which returns a float. This module, along with `base.py`, is used within a pytest setup to compare the outcomes of different API implementations, illustrating how tests can dynamically adapt to available modules.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/parametrize.rst

LANGUAGE: python
CODE:
```
def func1():
    return 1.0001
```

--------------------------------

TITLE: Pytest Output Showing Custom Static Report Header
DESCRIPTION: Displays the output of a Pytest run after `pytest_report_header` has been configured to return a static string. The custom header, 'project deps: mylib-1.1', is clearly visible in the session start information.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst

LANGUAGE: pytest
CODE:
```
$ pytest
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y
project deps: mylib-1.1
rootdir: /home/sweet/project
collected 0 items

========================== no tests ran in 0.12s ==========================
```

--------------------------------

TITLE: Install or Upgrade pytest using pip or easy_install
DESCRIPTION: These commands demonstrate how to install or upgrade the pytest testing framework using standard Python package managers. `pip` is the recommended tool, while `easy_install` is an alternative. Both commands ensure the latest version is installed.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-2.0.3.rst

LANGUAGE: shell
CODE:
```
pip install -U pytest
```

LANGUAGE: shell
CODE:
```
easy_install -U pytest
```

--------------------------------

TITLE: Define a Python function to fetch JSON from a URL
DESCRIPTION: This Python code defines a `get_json` function in `app.py` that takes a URL, makes an HTTP GET request using the `requests` library, and returns the JSON response. It serves as the target for subsequent monkeypatching examples.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/monkeypatch.rst

LANGUAGE: python
CODE:
```
# contents of app.py, a simple API retrieval example
import requests


def get_json(url):
    """Takes a URL, and returns the JSON."""
    r = requests.get(url)
    return r.json()
```

--------------------------------

TITLE: Install pytest prerelease via pip
DESCRIPTION: Instructs users on how to install a specific pytest prerelease version using pip, allowing them to test new features before the official release. Users should replace `{version}` with the actual prerelease version announced.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/scripts/release.pre.rst

LANGUAGE: bash
CODE:
```
pip install pytest=={version}
```

--------------------------------

TITLE: Install and Uninstall pytest Plugins (Bash)
DESCRIPTION: This snippet demonstrates how to install and uninstall pytest plugins using the 'pip' package manager in a bash environment. Once installed, pytest automatically discovers and integrates the plugin without further activation.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/plugins.rst

LANGUAGE: bash
CODE:
```
pip install pytest-NAME
pip uninstall pytest-NAME
```

--------------------------------

TITLE: Running Pytest and Observing Failure Output
DESCRIPTION: This command executes Pytest on the `test_module.py` file containing failing tests. The output illustrates Pytest's standard reporting for failed tests, including stack traces and a summary of the test session.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst

LANGUAGE: bash
CODE:
```
$ pytest test_module.py
```

LANGUAGE: text
CODE:
```
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 2 items

test_module.py FF                                                    [100%]

================================= FAILURES =================================
________________________________ test_fail1 ________________________________

tmp_path = PosixPath('PYTEST_TMPDIR/test_fail10')

    def test_fail1(tmp_path):
>       assert 0
E       assert 0

test_module.py:2: AssertionError
________________________________ test_fail2 ________________________________

    def test_fail2():
>       assert 0
E       assert 0

test_module.py:6: AssertionError
========================= short test summary info ==========================
FAILED test_module.py::test_fail1 - assert 0
FAILED test_module.py::test_fail2 - assert 0
============================ 2 failed in 0.12s ============================
```

--------------------------------

TITLE: Implement pytest xunit method-level setup and teardown methods
DESCRIPTION: These instance methods (`setup_method`, `teardown_method`) are called around each test method invocation within a class. They set up and tear down state tied to the execution of individual test methods. The `method` parameter is optional since pytest 3.0.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/xunit_setup.rst

LANGUAGE: python
CODE:
```
def setup_method(self, method):
    """setup any state tied to the execution of the given method in a
    class.  setup_method is invoked for every test method of a class.
    """


def teardown_method(self, method):
    """teardown any state that was previously setup with a setup_method
    call.
    """
```

--------------------------------

TITLE: Install Pytest Documentation Dependencies with pip
DESCRIPTION: This command installs all necessary Python packages required to build the pytest documentation. It utilizes the pip package manager to read and install dependencies listed in the `requirements-docs.txt` file.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/__wiki__/Docs-refactor.md

LANGUAGE: shell
CODE:
```
pip install -r requirements-docs.txt
```

--------------------------------

TITLE: Get pytest Help Interactively in Python
DESCRIPTION: This Python code demonstrates how to interactively access the help documentation for the pytest library directly from a Python prompt. It imports the pytest module and then uses the built-in `help()` function to display its documentation, which is useful for quick reference.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/builtin.rst

LANGUAGE: python
CODE:
```
import pytest

help(pytest)
```

--------------------------------

TITLE: Upgrade pytest using pip
DESCRIPTION: This command upgrades an existing pytest installation to the latest available version (3.0.1 or newer in this context) using Python's package installer, pip. It ensures you have the most up-to-date features and bug fixes.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-3.0.1.rst

LANGUAGE: shell
CODE:
```
pip install --upgrade pytest
```

--------------------------------

TITLE: Running Pytest with Fixture-Integrated Failure Reporting
DESCRIPTION: This command executes Pytest with the `-s` flag to display print statements from the custom fixture. It runs against the `test_module.py` which has tests failing in setup and call phases, demonstrating how the `conftest.py` plugin's fixture finalizer can intercept and print messages based on these specific failure stages before Pytest's default error and failure reports.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst

LANGUAGE: bash
CODE:
```
$ pytest -s test_module.py
```

LANGUAGE: text
CODE:
```
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 3 items

test_module.py Esetting up a test failed test_module.py::test_setup_fails
Fexecuting test failed or skipped test_module.py::test_call_fails
F

================================== ERRORS ==================================
____________________ ERROR at setup of test_setup_fails ____________________

    @pytest.fixture
    def other():
>       assert 0
E       assert 0

test_module.py:7: AssertionError
================================= FAILURES =================================
_____________________________ test_call_fails ______________________________

something = None

    def test_call_fails(something):
>       assert 0
E       assert 0

test_module.py:15: AssertionError
________________________________ test_fail2 ________________________________

    def test_fail2():
>       assert 0
E       assert 0

test_module.py:19: AssertionError
========================= short test summary info ==========================
FAILED test_module.py::test_call_fails - assert 0
FAILED test_module.py::test_fail2 - assert 0
```

--------------------------------

TITLE: Disable pytest Plugin Autoloading
DESCRIPTION: These examples show how to disable automatic plugin loading in pytest, requiring explicit specification of plugins. This can be achieved through environment variables, a command-line flag, or within the `pytest.ini` configuration file, allowing for granular control over plugin activation.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/plugins.rst

LANGUAGE: bash
CODE:
```
export PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
export PYTEST_PLUGINS=NAME,NAME2
pytest
```

LANGUAGE: bash
CODE:
```
pytest --disable-plugin-autoload -p NAME,NAME2
```

LANGUAGE: ini
CODE:
```
[pytest]
addopts =
        --disable-plugin-autoload
        -p NAME
        -p NAME2
```

--------------------------------

TITLE: Inspect Pytest Fixture Execution Order with --setup-plan
DESCRIPTION: Use the `pytest --setup-plan` command-line flag to visualize the execution order of fixtures for a given test file or specific test. This helps in understanding the dependency resolution and setup/teardown sequence. Adding `-v` provides more verbose output, including fixtures with names starting with an underscore.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/fixtures.rst

LANGUAGE: bash
CODE:
```
pytest --setup-plan test_something.py
```

LANGUAGE: bash
CODE:
```
pytest --setup-plan -v test_something.py
```

--------------------------------

TITLE: Example Doctest in a Text File
DESCRIPTION: This snippet illustrates a basic doctest defined within a plain text file. It demonstrates a simple Python interactive session where a variable is assigned and then evaluated, which pytest can discover and execute.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/doctest.rst

LANGUAGE: text
CODE:
```
# content of test_example.txt

hello this is a doctest
>>> x = 3
>>> x
3
```

--------------------------------

TITLE: Configure pytest.ini for pytester_example_dir (INI)
DESCRIPTION: This INI configuration sets the `pytester_example_dir` option in `pytest.ini`, which tells `pytester.copy_example` where to find example files. This is a crucial step for abstracting test content, ensuring that `pytester` can correctly locate and use external test files.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/writing_plugins.rst

LANGUAGE: ini
CODE:
```
# content of pytest.ini
[pytest]
pytester_example_dir = .
```

--------------------------------

TITLE: Install Tox for Test Environment Management
DESCRIPTION: This command installs `tox`, a command-line tool for automating testing and package building. Tox automatically sets up isolated virtual environments to run tests, ensuring consistent and reproducible testing conditions across different Python versions.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/CONTRIBUTING.rst

LANGUAGE: shell
CODE:
```
$ pip install tox
```

--------------------------------

TITLE: Install or Upgrade pytest using pip or easy_install
DESCRIPTION: This snippet shows how to install or upgrade the pytest testing framework using either `pip` (Python's package installer) or `easy_install`. The `-U` flag ensures that pytest is upgraded to the latest available version if already installed, or installed fresh otherwise.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-2.4.0.rst

LANGUAGE: bash
CODE:
```
pip install -U pytest # or
easy_install -U pytest
```

--------------------------------

TITLE: Use pytest acceptance test fixture in a test function (Python)
DESCRIPTION: This Python code demonstrates how to use the `accept` fixture in a pytest test function. It creates a subdirectory within the fixture's temporary directory and then uses the `accept.run` method to execute a shell command, asserting its output. This showcases an example of an acceptance test.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/attic.rst

LANGUAGE: python
CODE:
```
def test_some_acceptance_aspect(accept):
    accept.tmpdir.mkdir("somesub")
    result = accept.run("ls", "-la")
    assert "somesub" in result
```

--------------------------------

TITLE: Pytest Output After Dynamic Argument Modification
DESCRIPTION: This pytest output illustrates the effect of dynamically modifying pytest's command-line arguments via the `pytest_load_initial_conftests` hook. It shows pytest starting a test session with the automatically added parameters (e.g., for `pytest-xdist`), even if not explicitly provided by the user.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst

LANGUAGE: pytest
CODE:
```
pytest
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 0 items

========================== no tests ran in 0.12s ===========================
```

--------------------------------

TITLE: Define a Pytest test using pytester.copy_example (Python)
DESCRIPTION: This Python code defines a test file (`test_example.py`) that demonstrates the use of `pytester.copy_example` to include external test content. The `test_plugin` function copies the example file itself and then runs `pytest` with a specific keyword filter, showcasing how to programmatically execute and test abstracted logic.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/writing_plugins.rst

LANGUAGE: python
CODE:
```
# content of test_example.py


def test_plugin(pytester):
    pytester.copy_example("test_example.py")
    pytester.runpytest("-k", "test_example")


def test_example():
    pass
```

--------------------------------

TITLE: Implement pytest xunit class-level setup and teardown methods
DESCRIPTION: These class methods (`setup_class`, `teardown_class`) are invoked once before and after all test methods within a class. They manage state specific to the execution of the test class. They must be decorated with `@classmethod`.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/xunit_setup.rst

LANGUAGE: python
CODE:
```
@classmethod
def setup_class(cls):
    """setup any state specific to the execution of the given class (which
    usually contains tests).
    """


@classmethod
def teardown_class(cls):
    """teardown any state that was previously setup with a call to
    setup_class.
    """
```

--------------------------------

TITLE: Display pytest help and version information
DESCRIPTION: These commands provide various help and diagnostic information for pytest directly from the command line. They allow users to check the installed pytest version, view available built-in function arguments (fixtures), and access a comprehensive help message for all command-line and configuration file options.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/usage.rst

LANGUAGE: bash
CODE:
```
pytest --version   # shows where pytest was imported from
```

LANGUAGE: bash
CODE:
```
pytest --fixtures  # show available builtin function arguments
```

LANGUAGE: bash
CODE:
```
pytest -h | --help # show help on command line and config file options
```

--------------------------------

TITLE: Execute Pytest for a Test File and Observe Output
DESCRIPTION: This command-line example shows how to run a specific Pytest file. The output illustrates a test session, including collection, test execution, and the detailed failure report for an `assert 0` statement.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/tmp_path.rst

LANGUAGE: pytest
CODE:
```
$ pytest test_tmp_path.py
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 1 item

test_tmp_path.py F                                                   [100%]

================================= FAILURES =================================
_____________________________ test_create_file _____________________________

tmp_path = PosixPath('PYTEST_TMPDIR/test_create_file0')

    def test_create_file(tmp_path):
        d = tmp_path / "sub"
        d.mkdir()
        p = d / "hello.txt"
        p.write_text(CONTENT, encoding="utf-8")
        assert p.read_text(encoding="utf-8") == CONTENT
        assert len(list(tmp_path.iterdir())) == 1
>       assert 0
E       assert 0

test_tmp_path.py:11: AssertionError
========================= short test summary info ==========================
FAILED test_tmp_path.py::test_create_file - assert 0
============================ 1 failed in 0.12s ============================
```

--------------------------------

TITLE: Define a Sample pytest Plugin with a Configurable Fixture (Python)
DESCRIPTION: This Python code defines a sample pytest plugin that includes a command-line option and a fixture, serving as an example for testing with `pytester`. The `pytest_addoption` hook registers a `--name` option, allowing users to configure a default name. The `hello` fixture provides a function that returns a greeting string, optionally using the configured name or a provided argument, demonstrating fixture and configuration interaction.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/writing_plugins.rst

LANGUAGE: python
CODE:
```
import pytest


def pytest_addoption(parser):
    group = parser.getgroup("helloworld")
    group.addoption(
        "--name",
        action="store",
        dest="name",
        default="World",
        help='Default "name" for hello().',
    )


@pytest.fixture
def hello(request):
    name = request.config.getoption("name")

    def _hello(name=None):
        if not name:
            name = request.config.getoption("name")
        return f"Hello {name}!"

    return _hello
```

--------------------------------

TITLE: Implement pytest xunit function-level setup and teardown functions
DESCRIPTION: These functions (`setup_function`, `teardown_function`) are defined at the module level and invoked for every test function in the module. They manage state specific to the execution of individual test functions. The `function` parameter is optional since pytest 3.0.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/xunit_setup.rst

LANGUAGE: python
CODE:
```
def setup_function(function):
    """setup any state tied to the execution of the given function.
    Invoked for every test function in the module.
    """


def teardown_function(function):
    """teardown any state that was previously setup with a setup_function
    call.
    """
```

--------------------------------

TITLE: Use Print Statements for Debugging in Pytest Tests
DESCRIPTION: This Python example shows how `pytest` automatically captures `stdout` from `print` statements within test functions and their setup methods. It highlights a common debugging technique where `print` output is only displayed for failing tests, simplifying troubleshooting. The `setup_function` is run before each test.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/capture-stdout-stderr.rst

LANGUAGE: python
CODE:
```
# content of test_module.py


def setup_function(function):
    print("setting up", function)


def test_func1():
    assert True


def test_func2():
    assert False
```

--------------------------------

TITLE: Run Pytest Tests with Frozen Application (Bash)
DESCRIPTION: This bash command shows how to execute a test suite using a frozen application (`app_main`) that has pytest integrated into its entry point. The `--pytest` argument triggers the internal pytest runner, followed by standard pytest command-line options such as `--verbose`, `--tb=long`, and `--junit=xml=results.xml`, targeting a specific `test-suite/` directory. This allows for running tests directly against the packaged application.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst

LANGUAGE: bash
CODE:
```
./app_main --pytest --verbose --tb=long --junit=xml=results.xml test-suite/
```

--------------------------------

TITLE: Install pytest 8.0.0rc2 prerelease via pip
DESCRIPTION: This command installs the specified prerelease version of the pytest testing framework using pip. It's intended for testing new features and improvements before the final release, not for production use. Requires pip to be installed and available in the system's PATH.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-8.0.0rc2.rst

LANGUAGE: shell
CODE:
```
pip install pytest==8.0.0rc2
```

--------------------------------

TITLE: Python Test Classes with `callme` Method for Pre-Test Actions
DESCRIPTION: These Python examples define test classes, including `pytest` and `unittest` styles, that implement a static or class method named `callme`. This method is designed to be invoked by a session-scoped fixture before any tests within that class execute, demonstrating a pattern for class-specific setup or logging.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/special.rst

LANGUAGE: python
CODE:
```
# content of test_module.py


class TestHello:
    @classmethod
    def callme(cls):
        print("callme called!")

    def test_method1(self):
        print("test_method1 called")

    def test_method2(self):
        print("test_method2 called")


class TestOther:
    @classmethod
    def callme(cls):
        print("callme other called")

    def test_other(self):
        print("test other")


# works with unittest as well ...
import unittest


class SomeTest(unittest.TestCase):
    @classmethod
    def callme(self):
        print("SomeTest callme called")

    def test_unit1(self):
        print("test_unit1 method called")
```

--------------------------------

TITLE: Demonstrate Pytest Custom Option Validation Error
DESCRIPTION: This command shows the result of running pytest with an invalid value for a custom command-line option that has `choices` defined. Pytest automatically generates an error message, guiding the user to select from the valid options.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst

LANGUAGE: bash
CODE:
```
$ pytest -q --cmdopt=type3
```

--------------------------------

TITLE: Implement pytest xunit module-level setup and teardown functions
DESCRIPTION: These functions (`setup_module`, `teardown_module`) are called once for all test functions and classes within a module. They are used to set up and tear down state specific to the entire module's execution. The `module` parameter is optional since pytest 3.0.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/xunit_setup.rst

LANGUAGE: python
CODE:
```
def setup_module(module):
    """setup any state specific to the execution of the given module."""


def teardown_module(module):
    """teardown any state that was previously setup with a setup_module
    method.
    """
```

--------------------------------

TITLE: Install pytest 7.0.0rc1 Prerelease via pip
DESCRIPTION: This command installs the specified prerelease version of pytest (7.0.0rc1) using the pip package manager. It is intended for users who want to test new features before the final stable release. Ensure you have pip installed and your Python environment is active.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-7.0.0rc1.rst

LANGUAGE: bash
CODE:
```
pip install pytest==7.0.0rc1
```

--------------------------------

TITLE: Define pytest acceptance test fixture with custom option (Python)
DESCRIPTION: This Python code defines a pytest fixture for running acceptance tests. It introduces a `-A` command-line option to enable these tests. The `AcceptFixture` class manages a temporary directory and provides a `run` method to execute external commands. Tests are skipped if the `-A` option is not provided.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/attic.rst

LANGUAGE: python
CODE:
```
# ./conftest.py
def pytest_option(parser):
    group = parser.getgroup("myproject")
    group.addoption(
        "-A", dest="acceptance", action="store_true", help="run (slow) acceptance tests"
    )


def pytest_funcarg__accept(request):
    return AcceptFixture(request)


class AcceptFixture:
    def __init__(self, request):
        if not request.config.getoption("acceptance"):
            pytest.skip("specify -A to run acceptance tests")
        self.tmpdir = request.config.mktemp(request.function.__name__, numbered=True)

    def run(self, *cmd):
        """called by test code to execute an acceptance test."""
        self.tmpdir.chdir()
        return subprocess.check_output(cmd).decode()
```

--------------------------------

TITLE: Define an Artificial Slow Test Suite in Python
DESCRIPTION: Creates a Python test file (`test_some_are_slow.py`) containing multiple test functions with varying `time.sleep()` durations. This setup is designed to simulate a slow test suite, which is ideal for demonstrating Pytest's profiling capabilities.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst

LANGUAGE: python
CODE:
```
# content of test_some_are_slow.py
import time


def test_funcfast():
    time.sleep(0.1)


def test_funcslow1():
    time.sleep(0.2)


def test_funcslow2():
    time.sleep(0.3)
```

--------------------------------

TITLE: Run pytest to Execute Doctests from Text Files
DESCRIPTION: This command executes pytest which automatically discovers and runs doctests from `test*.txt` files in the current directory. The output shows a successful test run for the example `test_example.txt` file.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/doctest.rst

LANGUAGE: console
CODE:
```
$ pytest
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 1 item

test_example.txt .                                                   [100%]

============================ 1 passed in 0.12s =============================
```

--------------------------------

TITLE: Configure Pytest Command-Line Option Defaults
DESCRIPTION: This snippet demonstrates how to set default command-line options for pytest. You can use a `pytest.ini` file to specify options that will always be applied, or define the `PYTEST_ADDOPTS` environment variable for temporary additions. The example also shows how these options combine with explicit command-line arguments.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst

LANGUAGE: ini
CODE:
```
# content of pytest.ini
[pytest]
addopts = -ra -q
```

LANGUAGE: bash
CODE:
```
export PYTEST_ADDOPTS="-v"
```

LANGUAGE: bash
CODE:
```
pytest -m slow
```

LANGUAGE: bash
CODE:
```
pytest -ra -q -v -m slow
```

--------------------------------

TITLE: Pytest Console Output Demonstrating Captured stdout/stderr
DESCRIPTION: This console output illustrates `pytest`'s behavior when running tests with `print` statements, specifically how it displays captured `stdout` and `stderr`. It shows that output from successful tests is suppressed, while output from failing tests, including setup functions, is presented alongside the traceback. The output details the test session start, collected items, and the failure summary.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/capture-stdout-stderr.rst

LANGUAGE: plaintext
CODE:
```
$ pytest
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 2 items

test_module.py .F                                                    [100%]

================================= FAILURES =================================
________________________________ test_func2 ________________________________

    def test_func2():
>       assert False
E       assert False

test_module.py:12: AssertionError
-------------------------- Captured stdout setup ---------------------------
setting up <function test_func2 at 0xdeadbeef0001>
========================= short test summary info ==========================
FAILED test_module.py::test_func2 - assert False
======================= 1 failed, 1 passed in 0.12s ========================
```

--------------------------------

TITLE: Run Pytest and observe test session output (Pytest Command)
DESCRIPTION: This snippet shows the command-line execution of `pytest` and its standard output, confirming that the tests defined in `test_example.py` were collected and passed successfully. It illustrates the typical flow of running tests after configuring `pytester` and defining test functions, providing immediate feedback on test execution.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/writing_plugins.rst

LANGUAGE: pytest
CODE:
```
$ pytest
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
configfile: pytest.ini
collected 2 items

test_example.py ..                                                   [100%]

============================ 2 passed in 0.12s =============================
```

--------------------------------

TITLE: Install Python package in editable mode using pip
DESCRIPTION: This bash command installs the current Python package in 'editable' mode, linking the installed package directly to your source directory. This allows for immediate reflection of code changes without reinstallation, making it ideal for development and testing cycles.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/explanation/goodpractices.rst

LANGUAGE: bash
CODE:
```
pip install -e .
```

--------------------------------

TITLE: Python Base Module for API Comparison
DESCRIPTION: This `base.py` file provides a simple reference implementation of `func1()` returning an integer. It serves as a baseline for comparative testing against other potentially optimized or alternative implementations, as demonstrated in pytest's optional implementations feature.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/parametrize.rst

LANGUAGE: python
CODE:
```
def func1():
    return 1
```

--------------------------------

TITLE: Install or Upgrade pytest using pip
DESCRIPTION: This command demonstrates how to install or upgrade the pytest testing framework to the latest version using the pip package installer. It ensures that you have the most recent bug fixes and features.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-2.4.1.rst

LANGUAGE: bash
CODE:
```
pip install -U pytest
```

--------------------------------

TITLE: Dynamically Modify Pytest Command-Line Arguments via `pytest_load_initial_conftests` Hook
DESCRIPTION: This Python code, intended for an installable plugin, demonstrates how to dynamically modify pytest's command-line arguments using the `pytest_load_initial_conftests` hook. If the `pytest-xdist` plugin is detected, it calculates an optimal number of processes based on CPU count and prepends `"-n", str(num)` to the argument list, allowing for automatic parallel test execution.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst

LANGUAGE: python
CODE:
```
import sys


def pytest_load_initial_conftests(args):
    if "xdist" in sys.modules:  # pytest-xdist plugin
        import multiprocessing

        num = max(multiprocessing.cpu_count() / 2, 1)
        args[:] = ["-n", str(num)] + args
```

--------------------------------

TITLE: Conditionally skip all pytest tests in a class
DESCRIPTION: This Python example illustrates how to apply the `@pytest.mark.skipif` decorator to an entire test class. If the condition (e.g., `sys.platform == "win32"`) evaluates to `True`, all test methods within that class will be skipped. This prevents any setup or execution of the class's tests under the specified condition.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/skipping.rst

LANGUAGE: python
CODE:
```
@pytest.mark.skipif(sys.platform == "win32", reason="does not run on windows")
class TestPosixCalls:
    def test_function(self):
        "will not be setup or run under 'win32' platform"
```

--------------------------------

TITLE: Group multiple tests within a pytest class
DESCRIPTION: This Python code illustrates how to group multiple test functions (`test_one`, `test_two`) within a single class (`TestClass`) for better organization and context. Pytest automatically discovers methods prefixed with `test_` inside classes prefixed with `Test` without requiring inheritance.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/getting-started.rst

LANGUAGE: python
CODE:
```
# content of test_class.py
class TestClass:
    def test_one(self):
        x = "this"
        assert "h" in x

    def test_two(self):
        x = "hello"
        assert hasattr(x, "check")
```

--------------------------------

TITLE: Manage pytest Node Finalizers with addfinalizer() Helper
DESCRIPTION: The `node.addfinalizer()` helper method is introduced to be called during a node's setup phase. This ensures consistent finalizer behavior, preventing teardown execution if the corresponding setup fails.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-2.4.0.rst

LANGUAGE: python
CODE:
```
class MyNode:
    def setup(self):
        # ... setup logic ...
        self.addfinalizer(self.teardown)

    def teardown(self):
        # ... teardown logic ...
        pass
```

--------------------------------

TITLE: Permanently activate argcomplete for pytest in Bash
DESCRIPTION: This command registers `pytest` with `argcomplete` and appends the necessary activation script to the user's `.bashrc` file. This ensures persistent bash completion for `pytest` every time a new shell session is started.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/bash-completion.rst

LANGUAGE: bash
CODE:
```
register-python-argcomplete pytest >> ~/.bashrc
```

--------------------------------

TITLE: Apply Doctest Options Inline in an Example
DESCRIPTION: This snippet shows how to apply a `doctest` option, specifically `IGNORE_EXCEPTION_DETAIL`, directly within a doctest example using an inline comment. This allows for fine-grained control over how individual doctests behave, overriding global settings if necessary.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/doctest.rst

LANGUAGE: rst
CODE:
```
>>> something_that_raises()  # doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
ValueError: ...
```

--------------------------------

TITLE: Configure Pytest Plugin Entry Point in pyproject.toml
DESCRIPTION: This TOML configuration snippet shows how to define a `pytest11` entry point in a `pyproject.toml` file. This allows `pytest` to discover and load your plugin module automatically when the package is installed. Ensure the `myproject.pluginmodule` path correctly points to your plugin's main module.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/writing_plugins.rst

LANGUAGE: toml
CODE:
```
# sample ./pyproject.toml file
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "myproject"
classifiers = [
    "Framework :: Pytest",
]

[project.entry-points.pytest11]
myproject = "myproject.pluginmodule"
```

--------------------------------

TITLE: Example Pytest Test Module with `pytest.mark.slow` Marker
DESCRIPTION: This Python test module demonstrates how to apply the `pytest.mark.slow` marker to a test function (`test_func_slow`). This marker, when combined with the `conftest.py` configuration, allows for conditional skipping of tests based on a command-line option.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst

LANGUAGE: python
CODE:
```
# content of test_module.py
import pytest


def test_func_fast():
    pass


@pytest.mark.slow
def test_func_slow():
    pass
```

--------------------------------

TITLE: Pytest Module with Basic Failing Tests
DESCRIPTION: This Python module defines two simple Pytest functions, `test_fail1` and `test_fail2`, both intentionally failing with `assert 0`. `test_fail1` also demonstrates the use of the `tmp_path` fixture. This module serves as an example for testing the failure logging hook.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst

LANGUAGE: python
CODE:
```
    # content of test_module.py
    def test_fail1(tmp_path):
        assert 0


    def test_fail2():
        assert 0
```

--------------------------------

TITLE: List Available Pytest Fixtures and Descriptions
DESCRIPTION: Demonstrates how to use the `pytest --fixtures -v` command to list all available pytest fixtures, including those with leading underscores, along with their detailed descriptions. This output helps in understanding the functionality of various built-in and custom fixtures.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/builtin.rst

LANGUAGE: bash
CODE:
```
$ pytest  --fixtures -v
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y -- $PYTHON_PREFIX/bin/python
cachedir: .pytest_cache
rootdir: /home/sweet/project
collected 0 items
cache -- .../_pytest/cacheprovider.py:555
    Return a cache object that can persist state between testing sessions.

    cache.get(key, default)
    cache.set(key, value)

    Keys must be ``/`` separated strings, where the first part is usually the
    name of your plugin or application to avoid clashes with other cache users.

    Values can be any object handled by the json stdlib module.

capsys -- .../_pytest/capture.py:1000
    Enable text capturing of writes to ``sys.stdout`` and ``sys.stderr``.

    The captured output is made available via ``capsys.readouterr()`` method
    calls, which return a ``(out, err)`` namedtuple.
    ``out`` and ``err`` will be ``text`` objects.

    Returns an instance of :class:`CaptureFixture[str] <pytest.CaptureFixture>`.

    Example:

    .. code-block:: python

        def test_output(capsys):
            print("hello")
            captured = capsys.readouterr()
            assert captured.out == "hello\n"

capteesys -- .../_pytest/capture.py:1028
    Enable simultaneous text capturing and pass-through of writes
    to ``sys.stdout`` and ``sys.stderr`` as defined by ``--capture=``.


    The captured output is made available via ``capteesys.readouterr()`` method
    calls, which return a ``(out, err)`` namedtuple.
    ``out`` and ``err`` will be ``text`` objects.

    The output is also passed-through, allowing it to be "live-printed",
    reported, or both as defined by ``--capture=``.

    Returns an instance of :class:`CaptureFixture[str] <pytest.CaptureFixture>`.

    Example:

    .. code-block:: python

        def test_output(capteesys):
            print("hello")
            captured = capteesys.readouterr()
            assert captured.out == "hello\n"

capsysbinary -- .../_pytest/capture.py:1063
    Enable bytes capturing of writes to ``sys.stdout`` and ``sys.stderr``.

    The captured output is made available via ``capsysbinary.readouterr()``
    method calls, which return a ``(out, err)`` namedtuple.
    ``out`` and ``err`` will be ``bytes`` objects.

    Returns an instance of :class:`CaptureFixture[bytes] <pytest.CaptureFixture>`.

    Example:

    .. code-block:: python

        def test_output(capsysbinary):
            print("hello")
            captured = capsysbinary.readouterr()
            assert captured.out == b"hello\n"

capfd -- .../_pytest/capture.py:1091
    Enable text capturing of writes to file descriptors ``1`` and ``2``.

    The captured output is made available via ``capfd.readouterr()`` method
    calls, which return a ``(out, err)`` namedtuple.
    ``out`` and ``err`` will be ``text`` objects.

    Returns an instance of :class:`CaptureFixture[str] <pytest.CaptureFixture>`.

    Example:

    .. code-block:: python

        def test_system_echo(capfd):
            os.system('echo "hello"')
            captured = capfd.readouterr()
            assert captured.out == "hello\n"

capfdbinary -- .../_pytest/capture.py:1119
    Enable bytes capturing of writes to file descriptors ``1`` and ``2``.

    The captured output is made available via ``capfdbinary.readouterr()`` method
    calls, which return a ``(out, err)`` namedtuple.
    ``out`` and ``err`` will be ``byte`` objects.

    Returns an instance of :class:`CaptureFixture[bytes] <pytest.CaptureFixture>`.

    Example:

    .. code-block:: python

        def test_system_echo(capfdbinary):
            os.system('echo "hello"')
            captured = capfdbinary.readouterr()
            assert captured.out == b"hello\n"

doctest_namespace [session scope] -- .../_pytest/doctest.py:740
    Fixture that returns a :py:class:`dict` that will be injected into the
    namespace of doctests.

    Usually this fixture is used in conjunction with another ``autouse`` fixture:

    .. code-block:: python

        @pytest.fixture(autouse=True)
        def add_np(doctest_namespace):

```

--------------------------------

TITLE: Integrate Pytest into Frozen Application Entry Point (Python)
DESCRIPTION: This Python code illustrates how to make a frozen application serve as its own pytest runner. It checks for a `--pytest` argument to conditionally import and execute pytest, passing command-line arguments and explicitly registered plugins like `pytest_timeout`. This approach allows a single executable to handle both normal application logic and test execution, addressing the challenge of plugin discovery in frozen environments.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst

LANGUAGE: python
CODE:
```
# contents of app_main.py
import sys

import pytest_timeout  # Third party plugin

if len(sys.argv) > 1 and sys.argv[1] == "--pytest":
    import pytest

    sys.exit(pytest.main(sys.argv[2:], plugins=[pytest_timeout]))
else:
    # normal application execution: at this point argv can be parsed
    # by your argument-parsing library of choice as usual
    ...
```

--------------------------------

TITLE: Define and Use Hooks for Dynamic pytest_addoption (Python)
DESCRIPTION: This example demonstrates how to define a hook specification with `firstresult=True` in `hooks.py` to get a single default value for a command-line option. `myplugin.py` then registers these hooks and uses `pluginmanager.hook.pytest_config_file_default_value()` within `pytest_addoption` to dynamically retrieve the default value, allowing other plugins to influence option definitions.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/writing_hook_functions.rst

LANGUAGE: python
CODE:
```
# contents of hooks.py


# Use firstresult=True because we only want one plugin to define this
# default value
@hookspec(firstresult=True)
def pytest_config_file_default_value():
    """Return the default value for the config file command line option."""


# contents of myplugin.py


def pytest_addhooks(pluginmanager):
    """This example assumes the hooks are grouped in the 'hooks' module."""
    from . import hooks

    pluginmanager.add_hookspecs(hooks)


def pytest_addoption(parser, pluginmanager):
    default_value = pluginmanager.hook.pytest_config_file_default_value()
    parser.addoption(
        "--config-file",

```

--------------------------------

TITLE: Set Doctest Option Flags in pytest.ini
DESCRIPTION: This `pytest.ini` example demonstrates how to apply standard Python `doctest` module options globally for all doctests run by pytest. Here, `NORMALIZE_WHITESPACE` and `IGNORE_EXCEPTION_DETAIL` are enabled to make doctest comparisons more flexible.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/doctest.rst

LANGUAGE: ini
CODE:
```
[pytest]
doctest_optionflags = NORMALIZE_WHITESPACE IGNORE_EXCEPTION_DETAIL
```

--------------------------------

TITLE: Find Active pytest Plugins (Bash)
DESCRIPTION: This bash command helps identify which pytest plugins are currently active in your environment. Executing `pytest --trace-config` will output an extended test header showing activated plugins and any loaded local `conftest.py` files.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/plugins.rst

LANGUAGE: bash
CODE:
```
pytest --trace-config
```

--------------------------------

TITLE: Pytest Plugin to Access Test Results in Fixture Finalizers
DESCRIPTION: This `conftest.py` plugin demonstrates how to capture and make test execution reports accessible within fixture finalizers. It uses a `pytest_runtest_makereport` hook wrapper to stash `CollectReport` objects for each test phase. The `something` fixture then retrieves these reports in its teardown phase to print custom messages based on the outcome (failed or skipped) of the test's setup or call stages.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst

LANGUAGE: python
CODE:
```
    # content of conftest.py
    from typing import Dict
    import pytest
    from pytest import StashKey, CollectReport

    phase_report_key = StashKey[Dict[str, CollectReport]]()


    @pytest.hookimpl(wrapper=True, tryfirst=True)
    def pytest_runtest_makereport(item, call):
        # execute all other hooks to obtain the report object
        rep = yield

        # store test results for each phase of a call, which can
        # be "setup", "call", "teardown"
        item.stash.setdefault(phase_report_key, {})[rep.when] = rep

        return rep


    @pytest.fixture
    def something(request):
        yield
        # request.node is an "item" because we use the default
        # "function" scope
        report = request.node.stash[phase_report_key]
        if report["setup"].failed:
            print("setting up a test failed", request.node.nodeid)
        elif report["setup"].skipped:
            print("setting up a test skipped", request.node.nodeid)
        elif ("call" not in report) or report["call"].failed:
            print("executing test failed or skipped", request.node.nodeid)
```

--------------------------------

TITLE: Example Pytest Test Module with Incremental Marker
DESCRIPTION: This `test_step.py` file demonstrates the usage of the `incremental` marker on a test class. If `test_modification` fails (due to `assert 0`), `test_deletion` will be automatically marked as an expected failure and skipped, showcasing the incremental testing behavior configured in `conftest.py`.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst

LANGUAGE: python
CODE:
```
# content of test_step.py

import pytest


@pytest.mark.incremental
class TestUserHandling:
    def test_login(self):
        pass

    def test_modification(self):
        assert 0

    def test_deletion(self):
        pass


def test_normal():
    pass
```

--------------------------------

TITLE: Define recommended Python project test layout
DESCRIPTION: This text snippet illustrates a common and recommended project directory structure where tests are placed in a separate `tests/` directory, distinct from the application code within `src/mypkg/`. This separation improves organization and allows tests to run against either an installed or editable version of the package.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/explanation/goodpractices.rst

LANGUAGE: text
CODE:
```
pyproject.toml
src/
    mypkg/
        __init__.py
        app.py
        view.py
tests/
    test_app.py
    test_view.py
    ...
```

--------------------------------

TITLE: Execute unittest with pytest and observe output
DESCRIPTION: This bash command executes the specified Python test file (`test_unittest_db.py`) using pytest. It initiates a test session, which will run the `unittest.TestCase` classes and methods defined in the file. The output shown is the standard 'test session starts' message from pytest, indicating the beginning of the test execution.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/unittest.rst

LANGUAGE: bash
CODE:
```
$ pytest test_unittest_db.py
=========================== test session starts ============================
```

--------------------------------

TITLE: Demonstrate Pytest Test Class Instance Isolation and Attribute Sharing
DESCRIPTION: This snippet illustrates that pytest creates a unique instance of a test class for each test method, ensuring isolation between tests. However, it also highlights that class-level attributes are shared across these instances, which can lead to unexpected state if not properly managed, resulting in test failures if a test assumes an isolated class attribute state.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/getting-started.rst

LANGUAGE: python
CODE:
```
# content of test_class_demo.py
class TestClassDemoInstance:
    value = 0

    def test_one(self):
        self.value = 1
        assert self.value == 1

    def test_two(self):
        assert self.value == 1
```

LANGUAGE: pytest
CODE:
```
$ pytest -k TestClassDemoInstance -q
.F                                                                   [100%]
================================= FAILURES =================================
______________________ TestClassDemoInstance.test_two ______________________

self = <test_class_demo.TestClassDemoInstance object at 0xdeadbeef0002>

    def test_two(self):
>       assert self.value == 1
E       assert 0 == 1
E        +  where 0 = <test_class_demo.TestClassDemoInstance object at 0xdeadbeef0002>.value

test_class_demo.py:9: AssertionError
========================= short test summary info ==========================
FAILED test_class_demo.py::TestClassDemoInstance::test_two - assert 0 == 1
1 failed, 1 passed in 0.12s
```

--------------------------------

TITLE: Monitor Pytest Current Test Using psutil (Python)
DESCRIPTION: This Python script demonstrates how to monitor active pytest processes by inspecting the `PYTEST_CURRENT_TEST` environment variable using the `psutil` library. It iterates through all running processes, checks their environment variables, and prints details for processes where `PYTEST_CURRENT_TEST` is set. This is useful for identifying which test is currently running if a pytest session gets stuck.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst

LANGUAGE: python
CODE:
```
import psutil

for pid in psutil.pids():
    environ = psutil.Process(pid).environ()
    if "PYTEST_CURRENT_TEST" in environ:
        print(f'pytest process {pid} running: {environ["PYTEST_CURRENT_TEST"]}')
```

--------------------------------

TITLE: Call pytest.main() with custom plugin from Python code
DESCRIPTION: Illustrates how to register a custom plugin when invoking `pytest.main()` programmatically. The example defines a `MyPlugin` class with a `pytest_sessionfinish` hook and passes an instance of it to the `plugins` argument of `pytest.main()` to extend pytest's functionality.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/usage.rst

LANGUAGE: python
CODE:
```
# content of myinvoke.py
import sys

import pytest


class MyPlugin:
    def pytest_sessionfinish(self):
        print("*** test run reporting finishing")


if __name__ == "__main__":
    sys.exit(pytest.main(["-qq"], plugins=[MyPlugin()]))
```

--------------------------------

TITLE: Define and Use Pytest Fixtures with Dependencies
DESCRIPTION: This example demonstrates how to define pytest fixtures using `@pytest.fixture` and illustrates how fixtures can depend on each other. It includes a `Fruit` class for testing, a `my_fruit` fixture returning an instance, a `fruit_basket` fixture that uses `my_fruit`, and a test function `test_my_fruit_in_basket` that consumes both to verify the fruit's presence.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/explanation/fixtures.rst

LANGUAGE: python
CODE:
```
import pytest


class Fruit:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name


@pytest.fixture
def my_fruit():
    return Fruit("apple")


@pytest.fixture
def fruit_basket(my_fruit):
    return [Fruit("banana"), my_fruit]


def test_my_fruit_in_basket(my_fruit, fruit_basket):
    assert my_fruit in fruit_basket
```

--------------------------------

TITLE: Use string conditions for pytest.mark.skipif (Pre-Pytest 2.4)
DESCRIPTION: This Python example illustrates the older method of defining `skipif` conditions using a string, which is evaluated at test setup. This approach allows pytest to report a summary based on the condition string but can lead to issues with cross-importing markers due to reliance on module globals. It is still supported but boolean conditions are now preferred.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/historical-notes.rst

LANGUAGE: python
CODE:
```
import sys


@pytest.mark.skipif("sys.version_info >= (3,3)")
def test_function(): ...
```

--------------------------------

TITLE: Write Pytest Plugin Test with Pytester Fixture for Outcome Assertion
DESCRIPTION: This Python example demonstrates how to use the `pytester` fixture to create an inline test file and execute `pytest` against it, asserting the number of passed and failed tests.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/CONTRIBUTING.rst

LANGUAGE: python
CODE:
```
def test_true_assertion(pytester):
    pytester.makepyfile(
        """
        def test_foo():
            assert True
        """
    )
    result = pytester.runpytest()
    result.assert_outcomes(failed=0, passed=1)
```

--------------------------------

TITLE: Pytest Module for Comparing Optional Implementations
DESCRIPTION: This `test_module.py` defines a test function `test_func1` that accepts `basemod` and `optmod` fixtures. It asserts that the rounded results of `func1()` from both the base and optimized modules are equal, facilitating a robust comparison between different API implementations.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/parametrize.rst

LANGUAGE: python
CODE:
```
def test_func1(basemod, optmod):
    assert round(basemod.func1(), 3) == round(optmod.func1(), 3)
```

--------------------------------

TITLE: Define Pytest Tests with Platform-Specific Markers
DESCRIPTION: This Python test file contains example tests decorated with `pytest.mark` for different operating systems (darwin, linux, win32) and one test without any platform-specific marker. It serves as an input to demonstrate the platform-specific skipping plugin.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/markers.rst

LANGUAGE: python
CODE:
```
# content of test_plat.py

import pytest


@pytest.mark.darwin
def test_if_apple_is_evil():
    pass


@pytest.mark.linux
def test_if_linux_works():
    pass


@pytest.mark.win32
def test_if_win32_crashes():
    pass


def test_runs_everywhere():
    pass
```

--------------------------------

TITLE: Querying Recorded Warnings with pytest.warns Context Manager
DESCRIPTION: This example demonstrates how to use `pytest.warns` as a context manager to capture and query detailed information about raised warnings. It shows how to access the list of recorded warnings, check their count, and assert against specific message content, allowing for fine-grained verification.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/capture-warnings.rst

LANGUAGE: python
CODE:
```
with pytest.warns(RuntimeWarning) as record:
    warnings.warn("another warning", RuntimeWarning)

# check that only one warning was raised
assert len(record) == 1
# check that the message matches
assert record[0].message.args[0] == "another warning"
```

--------------------------------

TITLE: Deactivate or Unregister pytest Plugins
DESCRIPTION: These snippets demonstrate how to prevent specific pytest plugins from loading or to unregister them. This can be achieved via a command-line argument or by configuring the `pytest.ini` file, ensuring the named plugin will not be activated.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/plugins.rst

LANGUAGE: bash
CODE:
```
pytest -p no:NAME
```

LANGUAGE: ini
CODE:
```
[pytest]
addopts = -p no:NAME
```

--------------------------------

TITLE: Define Custom Type for Pytest Command-Line Option
DESCRIPTION: This Python code defines a custom type checker function (`type_checker`) for a pytest command-line option (`--cmdopt`). The function validates that the option's value starts with "type" and ends with a numeric string, raising a `pytest.UsageError` if validation fails. The `pytest_addoption` hook registers this custom option.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst

LANGUAGE: python
CODE:
```
import pytest


def type_checker(value):
    msg = "cmdopt must specify a numeric type as typeNNN"
    if not value.startswith("type"):
        raise pytest.UsageError(msg)
    try:
        int(value[4:])
    except ValueError:
        raise pytest.UsageError(msg)

    return value


def pytest_addoption(parser):
    parser.addoption(
        "--cmdopt",
        action="store",
        default="type1",
        help="my option: type1 or type2",
        type=type_checker,
    )
```

--------------------------------

TITLE: Define Custom Pytest Command-Line Option and Fixture
DESCRIPTION: This example illustrates how to create a custom command-line option and access its value within a test function via a pytest fixture. The `pytest_addoption` hook in `conftest.py` defines the new `--cmdopt` option, and a `cmdopt` fixture retrieves its configured value.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst

LANGUAGE: python
CODE:
```
# content of test_sample.py
def test_answer(cmdopt):
    if cmdopt == "type1":
        print("first")
    elif cmdopt == "type2":
        print("second")
    assert 0  # to see what was printed
```

LANGUAGE: python
CODE:
```
# content of conftest.py
import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--cmdopt", action="store", default="type1", help="my option: type1 or type2"
    )


@pytest.fixture
def cmdopt(request):
    return request.config.getoption("--cmdopt")
```

--------------------------------

TITLE: Demonstrate AssertionError from string.startswith comparison (Python)
DESCRIPTION: This test asserts that the string `s` ('123') starts with the string `g` ('456'). Since '123' does not start with '456', `s.startswith(g)` evaluates to `False`, causing the `assert` statement to fail with an `AssertionError`.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/reportingdemo.rst

LANGUAGE: python
CODE:
```
def test_startswith(self):
    s = "123"
    g = "456"
    assert s.startswith(g)
```

--------------------------------

TITLE: Example Python Docstring using Sphinx format
DESCRIPTION: This Python code snippet illustrates the Sphinx docstring format used in pytest for documenting functions. It shows how to include a concise summary, detailed explanation, parameter annotations, return values, raised exceptions, and versioning information. Type hints are used, making explicit type declarations in parameters optional.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/CONTRIBUTING.rst

LANGUAGE: python
CODE:
```
def my_function(arg: ArgType) -> Foo:
    """Do important stuff.

    More detailed info here, in separate paragraphs from the subject line.
    Use proper sentences -- start sentences with capital letters and end
    with periods.

    Can include annotated documentation:

    :param short_arg: An argument which determines stuff.
    :param long_arg:
        A long explanation which spans multiple lines, overflows
        like this.
    :returns: The result.
    :raises ValueError:
        Detailed information when this can happen.

    .. versionadded:: 6.0

    Including types into the annotations above is not necessary when
    type-hinting is being used (as in this example).
    """
```

--------------------------------

TITLE: Run Pytest with Hidden Tracebacks for Specific Functions
DESCRIPTION: Demonstrates a Pytest run where the traceback of the `checkconfig` function is hidden by default. The output shows a `ConfigException` failure without the full trace, indicating the default behavior for specific function calls.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst

LANGUAGE: pytest
CODE:
```
$ pytest -q test_checkconfig.py
F                                                                    [100%]
================================= FAILURES =================================
______________________________ test_something ______________________________

    def test_something():
>       checkconfig(42)
E       Failed: not configured: 42

test_checkconfig.py:11: Failed
========================= short test summary info ==========================
FAILED test_checkconfig.py::test_something - Failed: not configured: 42
1 failed in 0.12s
```

--------------------------------

TITLE: Execute pytest to Demonstrate Session Fixture and `callme` Invocation
DESCRIPTION: This command shows how to run `pytest` with the previously defined fixture and test modules, explicitly enabling output capturing (`-s`) to observe the execution flow. The output clearly illustrates the order of operations: fixture invocation, `callme` methods, and then individual test methods, confirming the pre-test class-level actions.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/special.rst

LANGUAGE: pytest
CODE:
```
$ pytest -q -s test_module.py
callattr_ahead_of_alltests called
callme called!
callme other called
SomeTest callme called
test_method1 called
.test_method2 called
.test other
.test_unit1 method called
.
4 passed in 0.12s
```

--------------------------------

TITLE: Run Pytest with Parametrized Test Failure
DESCRIPTION: This console output demonstrates running pytest on a parametrized test function that fails due to an assertion. It clearly shows how pytest reports the specific parametrized instance (e.g., '[1-2]') where the failure occurred, along with the detailed traceback.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/parametrize.rst

LANGUAGE: pytest
CODE:
```
$ pytest -q
F..
================================= FAILURES =================================
________________________ TestClass.test_equals[1-2] ________________________

self = <test_parametrize.TestClass object at 0xdeadbeef0002>, a = 1, b = 2

    def test_equals(self, a, b):
>       assert a == b
E       assert 1 == 2

test_parametrize.py:21: AssertionError
========================= short test summary info ==========================
FAILED test_parametrize.py::TestClass::test_equals[1-2] - assert 1 == 2
1 failed, 2 passed in 0.12s
```

--------------------------------

TITLE: Run Pytest with Custom Command-Line Options
DESCRIPTION: These commands demonstrate how to execute pytest tests while passing custom command-line options. The first command runs the test without specifying the custom option, relying on the default value. The second command explicitly provides a value for `--cmdopt` to alter the test's behavior.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst

LANGUAGE: bash
CODE:
```
$ pytest -q test_sample.py
```

LANGUAGE: bash
CODE:
```
$ pytest -q --cmdopt=type2
```

--------------------------------

TITLE: Use yaml.safe_load in Examples for Secure YAML Parsing
DESCRIPTION: To address issue 307, examples involving YAML parsing now explicitly use `yaml.safe_load`. This promotes secure parsing practices by avoiding the deserialization of untrusted YAML data, which could lead to arbitrary code execution.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-2.4.0.rst

LANGUAGE: python
CODE:
```
import yaml

malicious_yaml = "!!python/object/apply:os.system ['echo Hacked!']"
data = yaml.safe_load(malicious_yaml)
# Using yaml.safe_load prevents execution of the os.system command
print(data)
```

--------------------------------

TITLE: Pytest Conftest Fixtures for Optional Implementations
DESCRIPTION: This `conftest.py` snippet defines two session-scoped pytest fixtures, `basemod` and `optmod`. They leverage `pytest.importorskip` to conditionally import modules, allowing tests to be skipped gracefully if a specific implementation ('opt1', 'opt2') is not available, which is useful for comparing different API versions.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/parametrize.rst

LANGUAGE: python
CODE:
```
import pytest


@pytest.fixture(scope="session")
def basemod(request):
    return pytest.importorskip("base")


@pytest.fixture(scope="session", params=["opt1", "opt2"])
def optmod(request):
    return pytest.importorskip(request.param)
```

--------------------------------

TITLE: Demonstrate Previous Idioms for Negative Line Matching in pytest
DESCRIPTION: These Python code examples illustrate older methods used with `pytest.testdir` to assert that a test's standard output does not match a given pattern or contain specific text. The first example uses `re.match` to check for no regular expression match, while the second uses the `in` operator to check for the absence of a substring. These idioms are now superseded by the new `no_fnmatch_line` and `no_re_match_line` functions in `testdir` for improved failure output.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/changelog.rst

LANGUAGE: python
CODE:
```
result = testdir.runpytest()
assert re.match(pat, result.stdout.str()) is None
```

LANGUAGE: python
CODE:
```
result = testdir.runpytest()
assert text in result.stdout.str()
```

--------------------------------

TITLE: Post-process Pytest Test Reports Using `pytest_runtest_makereport` Hook
DESCRIPTION: This Python code snippet, intended for a `conftest.py` file, demonstrates how to implement a pytest hook `pytest_runtest_makereport` to customize test report generation. Using `wrapper=True` and `tryfirst=True`, it intercepts report creation, allowing for actions like appending details of failed test calls to a 'failures' file.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst

LANGUAGE: python
CODE:
```
# content of conftest.py

import os.path

import pytest


@pytest.hookimpl(wrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object
    rep = yield

    # we only look at actual failing test calls, not setup/teardown
    if rep.when == "call" and rep.failed:
        mode = "a" if os.path.exists("failures") else "w"
```

--------------------------------

TITLE: Add Static Information to Pytest Report Header via `conftest.py`
DESCRIPTION: Shows how to implement the `pytest_report_header` hook in `conftest.py` to return a static string. This string will be included directly in the Pytest test session header, useful for displaying project-specific metadata.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst

LANGUAGE: python
CODE:
```
# content of conftest.py


def pytest_report_header(config):
    return "project deps: mylib-1.1"
```

--------------------------------

TITLE: Run Pytest Deployment GitHub Workflow
DESCRIPTION: Initiates the Pytest deployment GitHub Actions workflow for a specified version. This job requires manual approval from the `pytest-dev/core` team before it proceeds to publish to PyPI and tag the repository.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/RELEASING.rst

LANGUAGE: bash
CODE:
```
$ gh workflow run deploy.yml -R pytest-dev/pytest --ref=release-{VERSION} -f version={VERSION}
```

--------------------------------

TITLE: Execute pytest to identify initial test failures
DESCRIPTION: This command line example shows how to run pytest with the `-q` (quiet) option to see the initial test results. It demonstrates the output when two of the 50 parameterized tests fail, including the summary of failed tests, before any re-run options are applied.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/cache.rst

LANGUAGE: pytest
CODE:
```
$ pytest -q
.................F.......F........................                   [100%]
================================= FAILURES =================================
_______________________________ test_num[17] _______________________________

i = 17

    @pytest.mark.parametrize("i", range(50))
    def test_num(i):
        if i in (17, 25):
>           pytest.fail("bad luck")
E           Failed: bad luck

test_50.py:7: Failed
_______________________________ test_num[25] _______________________________

i = 25

    @pytest.mark.parametrize("i", range(50))
    def test_num(i):
        if i in (17, 25):
>           pytest.fail("bad luck")
E           Failed: bad luck

test_50.py:7: Failed
========================= short test summary info ==========================
FAILED test_50.py::test_num[17] - Failed: bad luck
FAILED test_50.py::test_num[25] - Failed: bad luck
2 failed, 48 passed in 0.12s
```

--------------------------------

TITLE: Upgrade pytest using pip
DESCRIPTION: This command upgrades your existing pytest installation to the latest version available on PyPI. The '-U' flag ensures that the package is upgraded if already installed.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-2.5.0.rst

LANGUAGE: bash
CODE:
```
pip install -U pytest
```

--------------------------------

TITLE: Define and use custom pytest marker with plugin in Python
DESCRIPTION: This example demonstrates how to create a custom marker (`env`) and a command-line option (`-E`) within a `conftest.py` plugin. It shows registering the marker with `pytest_configure` and then filtering tests based on the marker's value and the command-line option using `pytest_runtest_setup`.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/markers.rst

LANGUAGE: python
CODE:
```
# content of conftest.py

import pytest


def pytest_addoption(parser):
    parser.addoption(
        "-E",
        action="store",
        metavar="NAME",
        help="only run tests matching the environment NAME.",
    )


def pytest_configure(config):
    # register an additional marker
    config.addinivalue_line(
        "markers", "env(name): mark test to run only on named environment"
    )


def pytest_runtest_setup(item):
    envnames = [mark.args[0] for mark in item.iter_markers(name="env")]
    if envnames:
        if item.config.getoption("-E") not in envnames:
```

--------------------------------

TITLE: Run pytest with Custom YAML Test File (Failing)
DESCRIPTION: Demonstrates executing custom YAML tests using pytest. This example shows a test session where one test fails and another passes, highlighting pytest's output format including failure details and a summary.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/nonpython.rst

LANGUAGE: console
CODE:
```
nonpython $ pytest test_simple.yaml
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y
rootdir: /home/sweet/project/nonpython
collected 2 items

test_simple.yaml F.                                                  [100%]

================================= FAILURES =================================
______________________________ usecase: hello ______________________________
usecase execution failed
   spec failed: 'some': 'other'
   no further details known at this point.
========================= short test summary info ==========================
FAILED test_simple.yaml::hello
======================= 1 failed, 1 passed in 0.12s ========================
```

--------------------------------

TITLE: Demonstrate Set Comparison Failure in Pytest (Python)
DESCRIPTION: Provides an example of a failing test involving set comparison in Pytest. It highlights Pytest's detailed output for assertion failures, showing differences between sets.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/assert.rst

LANGUAGE: python
CODE:
```
# content of test_assert2.py
def test_set_comparison():
    set1 = set("1308")
    set2 = set("8035")
    assert set1 == set2
```

--------------------------------

TITLE: Implement Custom Pytest Marker Hook in conftest.py
DESCRIPTION: This Python code defines `pytest_runtest_setup` in `conftest.py` to inspect markers on test items. It iterates through markers named 'my_marker', printing their details to stdout, which is flushed immediately for visibility during test setup.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/markers.rst

LANGUAGE: python
CODE:
```
# content of conftest.py
import sys


def pytest_runtest_setup(item):
    for marker in item.iter_markers(name="my_marker"):
        print(marker)
        sys.stdout.flush()
```

--------------------------------

TITLE: Require pytest Plugins in Test Module or Conftest File (Python)
DESCRIPTION: This Python snippet illustrates how to explicitly require plugins within a test module or a `conftest.py` file using the `pytest_plugins` global variable. When the module or conftest is loaded, the specified plugins will also be loaded.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/plugins.rst

LANGUAGE: python
CODE:
```
pytest_plugins = ("myapp.testsupport.myplugin",)
```

--------------------------------

TITLE: Start PDB debugger at the beginning of a pytest test
DESCRIPTION: This command configures pytest to drop into the Python Debugger (PDB) at the very beginning of each test. This is useful for stepping through a test from its initial state to understand its execution flow.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/failures.rst

LANGUAGE: bash
CODE:
```
pytest --trace
```

--------------------------------

TITLE: Upgrade pytest using pip
DESCRIPTION: This command upgrades your existing pytest installation to the latest version available on PyPI. The '-U' flag ensures that the package is upgraded if already installed.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-2.8.2.rst

LANGUAGE: bash
CODE:
```
pip install -U pytest
```

--------------------------------

TITLE: Implement a Custom Pytest Hook (Python)
DESCRIPTION: This function provides an example implementation for the previously defined `pytest_my_hook`. When placed in `conftest.py` or another plugin, it will be discovered and executed when the hook is called, printing the active hooks in this case.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/writing_hook_functions.rst

LANGUAGE: python
CODE:
```
def pytest_my_hook(config):
    """
    Print all active hooks to the screen.
    """
    print(config.hook)
```

--------------------------------

TITLE: Utilize Injected Namespace Objects in Python Doctests
DESCRIPTION: This Python docstring example demonstrates how to directly use objects that have been injected into the doctest namespace (e.g., `np` from the `doctest_namespace` fixture). This allows for cleaner and more concise doctests by providing pre-configured contexts.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/doctest.rst

LANGUAGE: python
CODE:
```
# content of numpy.py
def arange():
    """
    >>> a = np.arange(10)
    >>> len(a)
    10
    """
```

--------------------------------

TITLE: Example Pytest test_second.py for custom collection
DESCRIPTION: This Python file defines a simple pytest test function `test_2`. It is explicitly included in the `manifest.json` and will be collected by the custom directory collector.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/customdirectory.rst

LANGUAGE: python
CODE:
```
def test_2():
    assert True
```

--------------------------------

TITLE: Example Pytest test_first.py for custom collection
DESCRIPTION: This Python file defines a simple pytest test function `test_1`. It is explicitly included in the `manifest.json` and will be collected by the custom directory collector.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/customdirectory.rst

LANGUAGE: python
CODE:
```
def test_1():
    assert True
```

--------------------------------

TITLE: Run Pytest with Optional Module Import Skips
DESCRIPTION: This pytest command output shows the results of running `test_module.py` with skip reporting (`-rs`) enabled. It highlights that one test run was skipped because the 'opt2' module, required by a fixture, could not be imported, demonstrating pytest's ability to handle missing optional dependencies.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/parametrize.rst

LANGUAGE: pytest
CODE:
```
$ pytest -rs test_module.py
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 2 items

test_module.py .s                                                    [100%]

========================= short test summary info ==========================
SKIPPED [1] test_module.py:3: could not import 'opt2': No module named 'opt2'
======================= 1 passed, 1 skipped in 0.12s =======================
```

--------------------------------

TITLE: Build pytest documentation locally with Tox
DESCRIPTION: This command demonstrates how to build the pytest documentation locally using the 'tox' automation tool. After execution, the generated HTML documentation will be available in the 'doc/en/_build/html' directory, with 'en' indicating the documentation language.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/CONTRIBUTING.rst

LANGUAGE: bash
CODE:
```
$ tox -e docs
```

--------------------------------

TITLE: Honor --tb Style for Setup/Teardown Errors
DESCRIPTION: Issue 338 ensures that the `--tb` (traceback) style option is now honored for errors occurring during setup and teardown phases, not just during test execution. This provides consistent and desired traceback formatting across all stages of a test run.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-2.4.0.rst

LANGUAGE: bash
CODE:
```
# Show short tracebacks for all errors, including setup/teardown
pytest --tb=short
```

LANGUAGE: bash
CODE:
```
# Show no tracebacks
pytest --tb=no
```

--------------------------------

TITLE: Execute Pytest Tests and Observe Detailed Failure Output
DESCRIPTION: This command-line output demonstrates running pytest. The `$ pytest` command executes discovered tests, showing the test session start, collected items, and the failure of `test_answer`. pytest's assertion introspection provides a detailed breakdown of why the assertion `assert inc(3) == 5` failed, including the actual and expected values.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/README.rst

LANGUAGE: bash
CODE:
```
$ pytest
============================= test session starts =============================
collected 1 items

test_sample.py F

================================== FAILURES ===================================
_________________________________ test_answer _________________________________

    def test_answer():
>       assert inc(3) == 5
E       assert 4 == 5
E        +  where 4 = inc(3)

test_sample.py:5: AssertionError
========================== 1 failed in 0.04 seconds ===========================
```

--------------------------------

TITLE: Pytest Output with Conditional Verbose Report Header
DESCRIPTION: Illustrates the Pytest output when executed with the `-v` flag, showing the additional header lines returned by the verbose-aware `pytest_report_header` hook. This verifies the conditional display of extra information.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst

LANGUAGE: pytest
CODE:
```
$ pytest -v
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y -- $PYTHON_PREFIX/bin/python
cachedir: .pytest_cache
info1: did you know that ...
did you?
rootdir: /home/sweet/project
collecting ... collected 0 items

========================== no tests ran in 0.12s ==========================
```

--------------------------------

TITLE: Globally activate argcomplete for all Python applications
DESCRIPTION: This command enables `argcomplete` for all Python applications that support it across the system. It requires `sudo` privileges to modify system-wide configurations, providing completion for all compatible Python tools.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/bash-completion.rst

LANGUAGE: bash
CODE:
```
sudo activate-global-python-argcomplete
```

--------------------------------

TITLE: Introduce pytest_load_initial_conftests Hook for Plugins
DESCRIPTION: A new experimental hook, `pytest_load_initial_conftests`, has been added. This hook enables third-party plugins to execute code before any `conftest.py` files are loaded, allowing for earlier initialization and setup within the pytest process.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-2.4.0.rst

LANGUAGE: python
CODE:
```
# in a plugin or conftest.py
def pytest_load_initial_conftests():
    print("Executing initial conftest loading hook.")
    # Perform early plugin initialization or configuration here
```

--------------------------------

TITLE: Conditionally Skip All Tests in a Python Module
DESCRIPTION: Skip all tests in a module based on a specified condition using `pytest.mark.skipif`. This example skips tests if the operating system is Windows.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/skipping.rst

LANGUAGE: python
CODE:
```
pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="tests for linux only")
```

--------------------------------

TITLE: Use a Package-Scoped Pytest Fixture in a Test Module
DESCRIPTION: This Python code shows how a test function in `a/test_db.py` consumes the `db` fixture defined in `a/conftest.py`. The `db` object is passed as an argument to `test_a1`, demonstrating its availability within the package scope.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst

LANGUAGE: python
CODE:
```
# content of a/test_db.py
def test_a1(db):
    assert 0, db  # to show value
```

--------------------------------

TITLE: Configure pytest to Collect Doctests from Specific File Patterns
DESCRIPTION: This command line example shows how to instruct pytest to collect and run doctests from files matching a custom glob pattern, such as '*.rst', instead of the default 'test*.txt'. The `--doctest-glob` option can be used multiple times to include various patterns.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/doctest.rst

LANGUAGE: bash
CODE:
```
pytest --doctest-glob="*.rst"
```

--------------------------------

TITLE: Define a Package-Scoped Pytest Fixture in conftest.py
DESCRIPTION: This Python code defines a `db` fixture with a 'package' scope within a `conftest.py` file. The fixture instantiates a `DB` class, making a single `db` object available to all test modules within the same package. The `DB` class is a simple placeholder.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst

LANGUAGE: python
CODE:
```
# content of a/conftest.py
import pytest


class DB:
    pass


@pytest.fixture(scope="package")
def db():
    return DB()
```

--------------------------------

TITLE: Demonstrate direct ValueError raising (Python)
DESCRIPTION: This simple test explicitly raises a `ValueError` with a custom message. It serves as a straightforward example of how to manually raise an exception in Python, which is then captured by the test runner as a failure.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/reportingdemo.rst

LANGUAGE: python
CODE:
```
def test_raise(self):
    raise ValueError("demo error")
```

--------------------------------

TITLE: Pytest Run Output Showing Fixture Scope and Test Failures
DESCRIPTION: This console output captures the results of running `pytest` on the provided test modules. It displays assertions failing for `test_a1` and `test_a2` (to show the `db` object) and, critically, an `ERROR` for `b/test_error.py` indicating 'fixture 'db' not found', confirming the fixture's scope limitations.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst

LANGUAGE: console
CODE:
```
$ pytest
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 7 items

a/test_db.py F                                                       [ 14%]
a/test_db2.py F                                                      [ 28%]
b/test_error.py E                                                    [ 42%]
test_step.py .Fx.                                                    [100%]

================================== ERRORS ==================================
_______________________ ERROR at setup of test_root ________________________
file /home/sweet/project/b/test_error.py, line 1
  def test_root(db):  # no db here, will error out
E       fixture 'db' not found
>       available fixtures: cache, capfd, capfdbinary, caplog, capsys, capsysbinary, capteesys, doctest_namespace, monkeypatch, pytestconfig, record_property, record_testsuite_property, record_xml_attribute, recwarn, tmp_path, tmp_path_factory, tmpdir, tmpdir_factory
>       use 'pytest --fixtures [testpath]' for help on them.

/home/sweet/project/b/test_error.py:1
================================= FAILURES =================================
_________________________________ test_a1 __________________________________

db = <conftest.DB object at 0xdeadbeef0002>

    def test_a1(db):
>       assert 0, db  # to show value
        ^^^^^^^^^^^^
E       AssertionError: <conftest.DB object at 0xdeadbeef0002>
E       assert 0

a/test_db.py:2: AssertionError
_________________________________ test_a2 __________________________________

db = <conftest.DB object at 0xdeadbeef0002>

    def test_a2(db):
>       assert 0, db  # to show value
        ^^^^^^^^^^^^
E       AssertionError: <conftest.DB object at 0xdeadbeef0002>
E       assert 0

a/test_db2.py:2: AssertionError
____________________ TestUserHandling.test_modification ____________________

self = <test_step.TestUserHandling object at 0xdeadbeef0003>

    def test_modification(self):
>       assert 0
E       assert 0

test_step.py:11: AssertionError
========================= short test summary info ==========================
FAILED a/test_db.py::test_a1 - AssertionError: <conftest.DB object at 0x7...
FAILED a/test_db2.py::test_a2 - AssertionError: <conftest.DB object at 0x...
FAILED test_step.py::TestUserHandling::test_modification - assert 0
ERROR b/test_error.py::test_root
============= 3 failed, 2 passed, 1 xfailed, 1 error in 0.12s ==============
```

--------------------------------

TITLE: Skip All Tests in a Module If Import Missing (pytestmark)
DESCRIPTION: Similar to `pytest.importorskip`, `pytestmark` can be used with `pytest.importorskip` to skip an entire module if a dependency is missing. This example skips if 'pexpect' cannot be imported.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/skipping.rst

LANGUAGE: python
CODE:
```
pexpect = pytest.importorskip("pexpect")
```

--------------------------------

TITLE: Profile Pytest Test Durations with `--durations`
DESCRIPTION: Demonstrates using the `pytest --durations=N` command to identify and list the `N` slowest-executing test functions. The output clearly shows the tests from `test_some_are_slow.py` sorted by their execution time, aiding in performance optimization.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst

LANGUAGE: pytest
CODE:
```
$ pytest --durations=3
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 3 items

test_some_are_slow.py ...                                            [100%]

=========================== slowest 3 durations ============================
```

--------------------------------

TITLE: Pytest Output Without Conditional Verbose Report Header
DESCRIPTION: Shows the Pytest output when run without the verbose flag, confirming that the conditional header lines are not displayed. This highlights how `pytest_report_header` can tailor information based on runtime options.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst

LANGUAGE: pytest
CODE:
```
$ pytest
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 0 items

========================== no tests ran in 0.12s ==========================
```

--------------------------------

TITLE: Viewing Logged Failures in 'failures' File (Bash)
DESCRIPTION: This bash command displays the content of the 'failures' file, which was generated by the custom Pytest hook that logs failing test IDs. It shows the `nodeid` and `tmp_path` (if applicable) for each failed test.

SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst

LANGUAGE: bash
CODE:
```
$ cat failures
```

LANGUAGE: text
CODE:
```
test_module.py::test_fail1 (PYTEST_TMPDIR/test_fail10)
test_module.py::test_fail2
```