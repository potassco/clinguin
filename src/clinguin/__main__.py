"""
The main entry point for the application.
"""

import sys

from .utils.logging import configure_logging, get_logger
from .utils.parser import get_parser


def main() -> None:
    """
    Run the main function.
    """
    parser = get_parser()
    args = parser.parse_args()
    configure_logging(sys.stderr, args.log, sys.stderr.isatty())

    log = get_logger("main")
    log.info("info")
    log.warning("warning")
    log.debug("debug")
    log.error("error")


if __name__ == "__main__":
    main()
