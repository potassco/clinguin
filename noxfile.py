import os
import sys
import glob
import nox
import time

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
    """Run tests with proper coverage tracking inside Nox."""

    # Install dependencies
    args = [".[test]"]
    if EDITABLE_TESTS:
        args.insert(0, "-e")
    session.install(*args)

    # Run coverage tests
    session.run("coverage", "run", "-m", "pytest")

    # Wait for subprocesses to fully exit so that coverage is saved
    time.sleep(2)

    coverage_files = glob.glob(".coverage*")
    if coverage_files:
        session.run("coverage", "combine", "--quiet", *coverage_files)

    session.run("coverage", "report", "-m", "--fail-under=100")
