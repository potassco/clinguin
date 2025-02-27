"""
CLI module to start client and server from the command line.
"""

import sys
from clinguin.server.server import Server
from clinguin.client.client import Client

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
        client = Client(port=args.port, host=args.host, build=args.build, custom_path=args.custom_path)
        client.run()
