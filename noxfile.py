import os
import sys

import nox

nox.options.sessions = "lint_pylint", "typecheck", "test"

EDITABLE_TESTS = True
PYTHON_VERSIONS = None
if "GITHUB_ACTIONS" in os.environ:
    PYTHON_VERSIONS = ["3.9", "3.11"]
    EDITABLE_TESTS = False


@nox.session
def doc(session):
    """
    Build the documentation.

    Accepts the following arguments:
    - serve: open documentation after build
    - further arguments are passed to mkbuild
    """

    options = session.posargs[:]
    open_doc = "serve" in options
    if open_doc:
        options.remove("serve")

    session.install("-e", ".[doc]")

    if open_doc:
        open_cmd = "xdg-open" if sys.platform == "linux" else "open"
        session.run(open_cmd, "http://localhost:8000/systems/clinguin/")
        session.run("mkdocs", "serve", *options)
    else:
        session.run("mkdocs", "build", *options)


@nox.session
def dev(session):
    """
    Create a development environment in editable mode.

    Activate it by running `source .nox/dev/bin/activate`.
    """
    session.install("-e", ".[dev]")


@nox.session
def lint_pylint(session):
    """
    Run pylint.
    """
    session.install("-e", ".[lint_pylint]")
    session.run("pylint", "clinguin", "tests")


@nox.session
def typecheck(session):
    """
    Typecheck the code using mypy.
    """
    session.install("-e", ".[typecheck]")
    session.run("mypy", "--strict", "-p", "clinguin", "-p", "tests")


@nox.session(python=PYTHON_VERSIONS)
def test(session):
    """
    Run the tests.

    Accepts an additional arguments which are passed to the unittest module.
    This can for example be used to selectively run test cases.
    """

    args = [".[test]"]
    if EDITABLE_TESTS:
        args.insert(0, "-e")
    session.install(*args)
    if session.posargs:
        session.run("coverage", "run", "-m", "unittest", session.posargs[0], "-v")
    else:
        session.run("coverage", "run", "-m", "unittest", "discover", "-v")
        session.run("coverage", "report", "-m", "--fail-under=100")
