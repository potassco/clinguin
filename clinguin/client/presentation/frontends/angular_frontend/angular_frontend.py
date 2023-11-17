# pylint: disable=R1732
"""
Wrapper module for starting the angular frontend.
"""

import http.server
import json
import os
import signal
import socketserver
import webbrowser
from typing import Any

from clinguin.client import AbstractFrontend

_ROOT = os.path.abspath(os.path.dirname(__file__))

HTML_FILES_RELATIVE_DIRECTORY = "clinguin_angular_frontend"
SERVED_DIRECTORY = os.path.join(
    _ROOT,
    HTML_FILES_RELATIVE_DIRECTORY,
)


class Handler(http.server.SimpleHTTPRequestHandler):
    """
    Handler for backend, it sets the server directory as ''SERVED_DIRECTORY'',
    which corresponds to ''clinguin_angular_frontend''.
    """

    # pylint: disable=redefined-builtin
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=SERVED_DIRECTORY, **kwargs)

    def log_message(self, format: str, *args: Any) -> None:
        pass


class AngularFrontend(AbstractFrontend):
    """
    Class AngularFrontend extends like all other frontends the AbstractFrontend.
    It opens the angular server via ng serve.
    """

    @classmethod
    def register_options(cls, parser):
        parser.description = "This GUI is based on the Angular package."

        parser.add_argument(
            "--client-port",
            type=int,
            default=8087,
            help="Set the port for the webserver of the client.",
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

        with open(
            os.path.join(SERVED_DIRECTORY, "assets", "config.json"),
            "w",
            encoding="UTF-8",
        ) as config_file:
            config_file.write(str(json.dumps(config_dict)))

        socketserver.TCPServer.allow_reuse_address = True
        with socketserver.TCPServer(("", args.client_port), Handler) as httpd:
            print(
                f"\033[1;4m-> -> -> -> -> -> ->  Open the following link in your browser: \
                    \033[1;34m http://127.0.0.1:{args.client_port}\033[0m"
            )
            webbrowser.open(f"http://127.0.0.1:{args.client_port}", new=2)

            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("Interruption signal detected in frontend, shutting down!")
                try:
                    httpd.shutdown()
                    print("Frontend destruction successful!")
                except Exception:
                    print(
                        "Could not destroy frontend-server, frontend port could still be in use!"
                    )

                os.kill(os.getpid(), signal.SIGTERM)
