"""
The command line parser for the project.
"""

from argparse import ArgumentParser
from importlib import metadata
from textwrap import dedent
from typing import Any, Optional, cast

from . import logging

__all__ = ["get_parser"]

VERSION = metadata.version("clinguin")


def get_parser() -> ArgumentParser:
    """
    Return the parser for command line options.
    """
    parser = ArgumentParser(
        prog="clinguin",
        description=dedent(
            """\
            clinguin
            filldescription
            """
        ),
    )
    levels = [
        ("error", logging.ERROR),
        ("warning", logging.WARNING),
        ("info", logging.INFO),
        ("debug", logging.DEBUG),
    ]

    def get(levels: list[tuple[str, int]], name: str) -> Optional[int]:
        for key, val in levels:
            if key == name:
                return val
        return None  # nocoverage

    parser.add_argument(
        "--log",
        default="warning",
        choices=[val for _, val in levels],
        metavar=f"{{{','.join(key for key, _ in levels)}}}",
        help="set log level [%(default)s]",
        type=cast(Any, lambda name: get(levels, name)),
    )

    parser.add_argument("--version", "-v", action="version", version=f"%(prog)s {VERSION}")
    return parser
