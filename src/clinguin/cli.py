"""
CLI module to start client and server from the command line.
"""

import sys
import threading

from clinguin.client.client import Client
from clinguin.server.server import Server

from .utils.logging import configure_logging
from .utils.parser import get_parser


def main() -> None:
    """
    Run the main function.
    """
    parser = get_parser()
    args = parser.parse_args()

    configure_logging(sys.stderr, args.log, sys.stderr.isatty())
    if args.command == "server":
        args_cls = args.backend_class.args_class
        server = Server(
            backend_class=args.backend_class,
            backend_args=args_cls.from_args(args),
            port=args.port,
            host=args.host,
            multi=args.multi,
        )
        server.run()
    elif args.command == "client":
        client = Client(
            port=args.port,
            host=args.host,
            server_url=args.server_url,
            build=args.build,
            theme=args.theme,
            assets=args.assets,
        )
        client.run()
    elif args.command == "share":
        args_cls = args.backend_class.args_class
        server = Server(
            backend_class=args.backend_class,
            backend_args=args_cls.from_args(args),
            port=args.server_port,
            host=args.server_host,
            multi=args.multi,
        )
        client = Client(
            port=args.client_port,
            host=args.client_host,
            server_url=f"http://{args.server_host}:{args.server_port}",
            build=args.build,
            theme=args.theme,
            assets=args.assets,
        )

        server_thread = threading.Thread(target=server.run, name="clinguin-server", daemon=True)
        server_thread.start()

        print(f"Share URL: http://localhost:{args.client_port}")
        print(f"To expose it with ngrok: ngrok http {args.client_port}")
        client.run()
