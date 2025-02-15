"""
The command line parser for the project.
"""

from argparse import ArgumentParser, _SubParsersAction
from importlib import metadata
from typing import Any, Optional, cast

from rich_argparse import ArgumentDefaultsRichHelpFormatter
from rich.text import Text

from . import logging

__all__ = ["get_parser"]

ascii_art_clinguin = Text(
    r"""
         _   _                           _
   ___  | | (_)  _ __     __ _   _   _  (_)  _ __
  / __| | | | | | '_ \   / _` | | | | | | | | '_ \
 | (__  | | | | | | | | | (_| | | |_| | | | | | | |
  \___| |_| |_| |_| |_|  \__, |  \__,_| |_| |_| |_|
                         |___/
    """,
    no_wrap=True,
    justify="left",
)

ascii_art_server = Text(
    r"""
         __   ___  __        ___  __
        /__` |__  |__) \  / |__  |__)
        .__/ |___ |  \  \/  |___ |  \
    """,
    no_wrap=True,
    justify="left",
)

ascii_art_client = Text(
    r"""
         __          ___      ___
        /  ` |    | |__  |\ |  |
        \__, |___ | |___ | \|  |
    """,
    no_wrap=True,
    justify="left",
)

VERSION = metadata.version("clinguin")


def add_logger(parser: ArgumentParser) -> None:
    """
    Add the log level argument to the parser.
    Args:
        parser (ArgumentParser): The parser to add the argument to.
    """

    def get_level(levels: list[tuple[str, int]], name: str) -> Optional[int]:
        for key, val in levels:
            if key == name:
                return val
        return None  # nocoverage

    levels = [
        ("error", logging.ERROR),
        ("warning", logging.WARNING),
        ("info", logging.INFO),
        ("debug", logging.DEBUG),
    ]
    parser.add_argument(
        "--log",
        default="warning",
        choices=[val for _, val in levels],
        metavar=f"{{{','.join(key for key, _ in levels)}}}",
        help="Set log level [%(default)s]",
        type=cast(Any, lambda name: get_level(levels, name)),
    )


def setup_server_parser(subparsers: _SubParsersAction) -> None:  # type: ignore
    """
    Setup the parser for the server command.
    Args:
        subparsers (_SubParsersAction): The subparsers to add the server command to.
    """
    parser: ArgumentParser = subparsers.add_parser(
        "server",
        description=ascii_art_clinguin
        + ascii_art_server
        + "\n🚀 Start the server for clinguin.\
        \n It will use the domain encodings to reason and the ui encodings to define the UI.",  # type: ignore
        help="Start the server",
        formatter_class=ArgumentDefaultsRichHelpFormatter,
    )
    add_logger(parser)

    parser.add_argument(
        "--multi",
        action="store_true",
        help="Enable multiple backend instances per client connection.",
    )

    parser.add_argument(
        "--backend",
        type=str,
        metavar="",  # Suppress metavar display in help
        help="Specify the backend class name to use.",
        default="ClingoBackend",
    )

    parser.add_argument(
        "--custom-classes",
        type=str,
        metavar="",
        help="Path to a directory containing custom backend classes.",
    )

    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        metavar="",
        help="Set the server port.",
    )

    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",  # Default to localhost
        metavar="",
        help="Specify the server host. Use 0.0.0.0 for external access.",
    )


def setup_client_parser(subparsers: _SubParsersAction) -> None:  # type: ignore
    """
    Setup the parser for the client command.
    Args:
        subparsers (_SubParsersAction): The subparsers to add the client command to.
    """
    parser: ArgumentParser = subparsers.add_parser(
        "client",
        description=ascii_art_clinguin
        + ascii_art_client
        + "\n🚀 Start the client for clinguin.\
        \n It will run Angular to render the UI and react to events.",  # type: ignore
        help="Start the client",
        formatter_class=ArgumentDefaultsRichHelpFormatter,
    )
    add_logger(parser)
    parser.add_argument(
        "--port",
        type=int,
        default=8001,
        metavar="",
        help="Port to serve the client",
    )

    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        metavar="",
        help="Host to bind the client to. Use 0.0.0.0 for external access.",
    )

    parser.add_argument(
        "--server-url",
        type=str,
        default="http://127.0.0.1:8000",
        metavar="",
        help="Full URL of the Clinguin Server to connect to.",
    )

    parser.add_argument(
        "--build",
        action="store_true",
        help="Rebuild the Angular frontend before serving. Requires installing Angular CLI.",
    )

    parser.add_argument(
        "--custom-path",
        type=str,
        metavar="",
        help="Path to custom frontend files to include before building.",
    )


def get_parser() -> ArgumentParser:
    """
    Return the parser for command line options.
    """
    parser = ArgumentParser(
        description=ascii_art_clinguin + "\n🚀 Clinguin CLI - Start the server or client."
        "\nUse: clinguin server or clinguin client",  # type: ignore
        formatter_class=ArgumentDefaultsRichHelpFormatter,
    )

    parser.add_argument("--version", "-v", action="version", version=f"%(prog)s {VERSION}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    setup_server_parser(subparsers)
    setup_client_parser(subparsers)
    return parser
