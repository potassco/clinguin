"""
Test cases for main application functionality.
"""

from io import StringIO
from unittest import TestCase

from clinguin.utils import logging
from clinguin.utils.logging import configure_logging, get_logger
from clinguin.utils.parser import get_parser


class TestMain(TestCase):
    """
    Test cases for main application functionality.
    """

    def test_logger(self) -> None:
        """
        Test the logger.
        """
        sio = StringIO()
        configure_logging(sio, logging.INFO, True)
        log = get_logger("main")
        log.info("test123")
        self.assertRegex(sio.getvalue(), "test123")

    def test_parser(self) -> None:
        """
        Test the parser.
        """
        parser = get_parser()
        ret = parser.parse_args(["--log", "info"])
        self.assertEqual(ret.log, logging.INFO)
