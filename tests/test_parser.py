"""
Test the argument parser for the clinguin package.
"""

import pytest
from clinguin.utils.parser import get_parser
from clinguin.utils import logging  # Import your logging module


@pytest.mark.parametrize(
    "log_level, expected",
    [
        ("error", logging.ERROR),
        ("warning", logging.WARNING),
        ("info", logging.INFO),
        ("debug", logging.DEBUG),
    ],
)
def test_client_log_level(log_level, expected):
    """Test if the --log argument correctly sets log level."""
    parser = get_parser()
    args = parser.parse_args(["client", "--log", log_level])
    assert args.log == expected


def test_server_default_port():
    """Ensure default port is 8000 for the server."""
    parser = get_parser()
    args = parser.parse_args(["server"])
    assert args.port == 8000


def test_client_custom_port():
    """Check if client correctly sets a custom port."""
    parser = get_parser()
    args = parser.parse_args(["client", "--port", "9001"])
    assert args.port == 9001


def test_client_default_host():
    """Ensure default host is 127.0.0.1 for the client."""
    parser = get_parser()
    args = parser.parse_args(["client"])
    assert args.host == "127.0.0.1"


def test_server_custom_host():
    """Check if the server correctly sets a custom host."""
    parser = get_parser()
    args = parser.parse_args(["server", "--host", "0.0.0.0"])
    assert args.host == "0.0.0.0"


def test_client_server_url():
    """Ensure the client correctly sets a custom server URL."""
    parser = get_parser()
    args = parser.parse_args(["client", "--server-url", "http://192.168.1.100:8000"])
    assert args.server_url == "http://192.168.1.100:8000"


def test_client_missing_command():
    """Ensure the parser fails when no command is provided."""
    parser = get_parser()
    with pytest.raises(SystemExit):  # argparse exits on missing required args
        parser.parse_args([])
