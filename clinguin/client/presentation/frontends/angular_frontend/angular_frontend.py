# pylint: disable=R1732
"""
Wrapper module for starting the angular frontend.
"""
import sys
import inspect
import pathlib
import subprocess

import http.server
import socketserver

from clinguin.client import AbstractFrontend

DIRECTORY = "clinguin/client/presentation/frontends/angular_frontend/clinguin_angular_frontend"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

class AngularFrontend(AbstractFrontend):
    """
    Class AngularFrontend extends like all other frontends the AbstractFrontend.
    It opens the angular server via ng serve.
    """

    def __init__(self, args, base_engine):
        super().__init__(base_engine, args)

        port = 10001

        with socketserver.TCPServer(("",port), Handler) as httpd:
            print("serving at port", port)
            httpd.serve_forever()


        # Just for local development!


        path = pathlib.Path(inspect.getfile(AngularFrontend)).parent.parent.parent.parent.parent.parent\
            / "angular_frontend"

        if sys.platform.startswith("win32") or sys.platform.startswith("cygwin"):
            self.process = subprocess.Popen(["ng", "serve"], shell=True, cwd=path)
        else:
            self.process = subprocess.Popen(["ng", "serve"], cwd=path)

        self.process.communicate()
