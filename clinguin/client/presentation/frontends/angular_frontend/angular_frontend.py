# pylint: disable=R1732
"""
Wrapper module for starting the angular frontend.
"""

import os
import json
import signal

import http.server
import socketserver

from clinguin.client import AbstractFrontend

HTML_FILES_RELATIVE_DIRECTORY = "clinguin_angular_frontend"
SERVED_DIRECTORY = os.path.join("clinguin","client","presentation","frontends","angular_frontend",HTML_FILES_RELATIVE_DIRECTORY)

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=SERVED_DIRECTORY, **kwargs)

class AngularFrontend(AbstractFrontend):
    """
    Class AngularFrontend extends like all other frontends the AbstractFrontend.
    It opens the angular server via ng serve.
    """

    @classmethod
    def register_options(cls, parser):
        parser.description = (
            "This GUI is based on the Angular package."
        )

        parser.add_argument(
            "--client-port", type=int, default=8080, help="Set the port for the webserver of the client."
        )

    def __init__(self, base_engine, args):
        super().__init__(base_engine, args)

        if hasattr(args, "server_port"):
            server_port = args.server_port
        else:
            server_port = 8000

        if hasattr(args, "server_url"):
            server_url = args.server_url
        else:
            server_url = "http://localhost"

        config_dict = {}
        config_dict["serverPort"] = server_port
        config_dict["serverUrl"] = server_url

        with open(os.path.join(SERVED_DIRECTORY,"assets","config.json"), "w") as config_file:
            config_file.write(str(json.dumps(config_dict)))

        with socketserver.TCPServer(("", args.client_port), Handler) as httpd:
            print("serving at port", args.client_port)
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("Interruption signal detected in frontend, shutting down!")
                try:
                    httpd.shutdown()
                    print("Frontend destruction successful!")
                except Exception as ex:
                    print("Could not destroy frontend-server, frontend port could still be in use!")
                
                os.kill(os.getpid(), signal.SIGTERM)
