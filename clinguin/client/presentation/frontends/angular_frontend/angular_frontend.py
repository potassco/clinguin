# pylint: disable=R1732
"""
Wrapper module for starting the angular frontend.
"""
import sys
import inspect
import pathlib
import subprocess

from clinguin.client import AbstractFrontend


class AngularFrontend(AbstractFrontend):
    """
    Class AngularFrontend extends like all other frontends the AbstractFrontend.
    It opens the angular server via ng serve.
    """

    def __init__(self, args, base_engine):
        super().__init__(base_engine, args)
        path = pathlib.Path(inspect.getfile(AngularFrontend)).parent.parent.parent.parent.parent.parent\
            / "angular_frontend"
        print(path)

        if sys.platform.startswith("win32") or sys.platform.startswith("cygwin"):
            self.process = subprocess.Popen(["ng", "serve"], shell=True, cwd=path)
        else:
            self.process = subprocess.Popen(["ng", "serve"], cwd=path)

        self.process.communicate()
