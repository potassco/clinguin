"""
Test the argument parser for the clinguin package.
"""

import os
import sys
import tempfile
from unittest.mock import MagicMock, patch

import pytest

from clinguin.server.backends import ClingoBackend
from clinguin.utils import logging
from clinguin.utils.parser import (
    find_backend_classes,
    get_backend_from_sysargv,
    get_custom_backends_directory,
    get_parser,
    lazy_import_backend,
    setup_server_parser,
)


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


def test_lazy_import_backend_clingo_backend():
    """Test lazy import of ClingoBackend."""
    result = lazy_import_backend("ClingoBackend", {})
    assert result is ClingoBackend


def test_lazy_import_backend_class_not_found():
    """Test lazy import when backend class is not found."""
    with pytest.raises(ImportError, match="Backend class 'NonExistentBackend' not found"):
        lazy_import_backend("NonExistentBackend", {})


@pytest.mark.parametrize(
    "mock_spec, error",
    [
        (None, "could not be loaded"),
        (MagicMock(loader=None), "could not be loaded"),
    ],
)
def test_lazy_import_backend_load_errors(mock_spec, error):
    """Test lazy import when module cannot be loaded."""
    with patch("importlib.util.spec_from_file_location", return_value=mock_spec):
        with pytest.raises(ImportError, match=error):
            lazy_import_backend("CustomBackend", {"CustomBackend": "path.py"})


def test_lazy_import_backend_module_not_found():
    """Test lazy import when module cannot be found."""
    backends_dict = {"CustomBackend": "path.py"}
    with patch("importlib.util.spec_from_file_location") as mock_spec:
        mock_spec.return_value.loader.exec_module.side_effect = ModuleNotFoundError("Error")
        with patch("builtins.print") as mock_print:
            with pytest.raises(ModuleNotFoundError):
                lazy_import_backend("CustomBackend", backends_dict)
            mock_print.assert_called_once()


@pytest.mark.parametrize(
    "module_content, error",
    [
        (type("MockModule", (), {"CustomBackend": type("NotABackend", (), {})}), "not a subclass"),
        (type("MockModule", (), {}), "not a subclass"),
    ],
)
def test_lazy_import_backend_class_errors(module_content, error):
    """Test lazy import when class is not a subclass of ClingoBackend."""
    backends_dict = {"CustomBackend": "path.py"}
    with patch("importlib.util.spec_from_file_location"):
        with patch("importlib.util.module_from_spec", return_value=module_content):
            with pytest.raises(ImportError, match=error):
                lazy_import_backend("CustomBackend", backends_dict)


def test_lazy_import_backend_success():
    """Test successful lazy import of a custom backend."""

    class CustomBackend(ClingoBackend):
        pass

    module = type("MockModule", (), {"CustomBackend": CustomBackend})
    with patch("importlib.util.spec_from_file_location"):
        with patch("importlib.util.module_from_spec", return_value=module):
            result = lazy_import_backend("CustomBackend", {"CustomBackend": "path.py"})
            assert result is CustomBackend


def test_find_backend_classes_valid():
    """Test finding backend classes in a valid directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, "test.py")
        with open(test_file, "w") as f:
            f.write("class TestBackend(ClingoBackend): pass\nclass AnotherBackend(TestBackend): pass")
        result = find_backend_classes([tmpdir])
        assert {"TestBackend", "AnotherBackend"} <= set(result.keys())


def test_find_backend_classes_nonexistent_dir():
    """Test finding backend classes in a non-existent directory."""
    with pytest.raises(FileNotFoundError):
        find_backend_classes(["/nonexistent"])


def test_find_backend_classes_empty():
    """Test finding backend classes in an empty directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        assert find_backend_classes([tmpdir]) == {}


def test_find_backend_classes_circular():
    """Test finding backend classes with circular dependencies."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, "circular.py")
        with open(test_file, "w") as f:
            f.write("class A(B): pass\nclass B(A): pass")
        assert isinstance(find_backend_classes([tmpdir]), dict)


@pytest.mark.parametrize(
    "argv, expected",
    [
        (["clinguin", "server", "--backend", "Custom"], "Custom"),
        (["clinguin", "server", "--backend"], "ClingoBackend"),
        (["clinguin", "server"], "ClingoBackend"),
    ],
)
def test_get_backend_from_sysargv(argv, expected):
    """Test getting backend from sys.argv."""
    with patch.object(sys, "argv", argv):
        assert get_backend_from_sysargv() == expected


@pytest.mark.parametrize(
    "argv, expected",
    [
        (["clinguin", "server", "--custom-backends-dir", "/dir"], "/dir"),
        (["clinguin", "server", "--custom-backends-dir"], None),
        (["clinguin", "server"], None),
    ],
)
def test_get_custom_backends_directory(argv, expected):
    """Test getting custom backends directory from sys.argv."""
    with patch.object(sys, "argv", argv):
        assert get_custom_backends_directory() == expected


def test_setup_server_parser_custom_dir():
    """Test setup_server_parser with custom backends directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        with patch.object(sys, "argv", ["clinguin", "server", "--custom-backends-dir", tmpdir]):
            with (
                patch("clinguin.utils.parser.get_default_backend_path", return_value="/default") as mock_default_path,
                patch("clinguin.utils.parser.find_backend_classes") as mock_find,
                patch("clinguin.utils.parser.lazy_import_backend"),
            ):

                mock_find.return_value = {}
                mock_subparsers = MagicMock()
                setup_server_parser(mock_subparsers)

                dirs = mock_find.call_args[0][0]
                assert tmpdir in dirs and "/default" in dirs


def test_find_backend_classes_duplicates():
    """Test finding backend classes with duplicate names in different directories."""
    with tempfile.TemporaryDirectory() as dir1, tempfile.TemporaryDirectory() as dir2:
        file1 = os.path.join(dir1, "f1.py")
        with open(file1, "w") as f:
            f.write("class DupBackend(ClingoBackend): pass")
        file2 = os.path.join(dir2, "f2.py")
        with open(file2, "w") as f:
            f.write("class DupBackend(ClingoBackend): pass")
        result = find_backend_classes([dir1, dir2])
        assert result == {"DupBackend": file1}
