"""
Nox sessions for linting, type checking and testing.
"""

import os

import nox  # type: ignore

nox.options.sessions = "lint", "typecheck", "test"
nox.options.default_venv_backend = "uv|virtualenv"

PYTHON_VERSIONS = None
if "GITHUB_ACTIONS" in os.environ:
    PYTHON_VERSIONS = ["3.10", "3.14"]


@nox.session
def dev(session):
    """
    Create a development environment in editable mode.

    Activate it by running `source .nox/dev/bin/activate`.
    """
    session.install("-e", ".[dev]")


@nox.session
def lint(session):
    """
    Run ruff.
    """
    if not session.virtualenv._reused:
        session.install(".[lint]")
    session.run("ruff", "check")
    session.run("ruff", "format", "--check")


@nox.session
def typecheck(session):
    """
    Typecheck the code using mypy.
    """
    if not session.virtualenv._reused:
        session.install(".[typecheck]")
    session.run("ty", "check")


@nox.session(python=PYTHON_VERSIONS)
def test(session):
    """
    Run the tests.

    Accepts additional arguments which are passed to the pytest module. This
    can for example be used to selectively run test cases via option `-k`.
    """
    if not session.virtualenv._reused:
        session.install(".[test]")
    if session.posargs:
        session.run("pytest", "-v", *session.posargs)
    else:
        session.run("pytest", "--cov", "-v")
