"""
Test cases for main application functionality using pytest.
"""

import pytest

from clinguin.utils import logging
from clinguin.utils.logging import get_logger
from clinguin.utils.parser import get_parser


@pytest.mark.filterwarnings("ignore")
@pytest.mark.usefixtures("caplog")
def test_logger(caplog: pytest.LogCaptureFixture):
    """Test that logger correctly logs messages."""
    with caplog.at_level(logging.INFO):
        log = get_logger("main")
        log.info("test123")

    assert "test123" in caplog.text


def test_parser():
    """Test the parser handles log level arguments correctly."""
    parser = get_parser()
    ret = parser.parse_args(["--log", "info"])
    assert ret.log == logging.INFO
