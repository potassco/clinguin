import os

import nox

# default sessions that shall be run
nox.options.sessions = ["test"]



EDITABLE_TESTS = True
PYTHON_VERSIONS = None
if "GITHUB_ACTIONS" in os.environ:
    PYTHON_VERSIONS = ["3.10"]
    EDITABLE_TESTS = False

@nox.session(python=PYTHON_VERSIONS)
def test(session):
    session.install("pytest")
    session.install(".")
    session.run("pytest")


    
