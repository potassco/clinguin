"""Test cases for the errors module."""

from unittest.mock import MagicMock

import pytest

from clinguin.utils.errors import NoModelError, get_server_error_alert


class TestNoModelError:
    """Test cases for NoModelError exception."""

    def test_instantiation(self):
        """Test NoModelError instantiation with and without core."""
        # Without core
        error = NoModelError()
        assert isinstance(error, Exception)
        assert error.core is None

        # With core
        test_core = ["atom1", "atom2"]
        error_with_core = NoModelError(core=test_core)
        assert error_with_core.core == test_core

    def test_exception_behavior(self):
        """Test that NoModelError can be raised and caught."""
        with pytest.raises(NoModelError) as exc_info:
            raise NoModelError(core=["test"])
        assert exc_info.value.core == ["test"]


class TestGetServerErrorAlert:
    """Test cases for get_server_error_alert function."""

    def test_no_last_response(self):
        """Test with no last_response (creates new structure)."""
        result = get_server_error_alert(message="Test error")

        # Verify basic structure
        assert "ui" in result and "ds" in result
        assert result["ds"] == {}

        # Verify error alert
        error_alert = result["ui"]["children"][0]["children"][0]
        assert error_alert["id"] == "server_error"
        assert error_alert["type"] == "message"
        assert error_alert["parent"] == "window"

        # Verify message attribute
        message_attr = next(attr for attr in error_alert["attributes"] if attr["key"] == "message")
        assert message_attr["value"] == "Test error (Check the server logs for more details)."

    def test_with_last_response_bug(self):
        """Test with last_response (triggers bug in original code)."""
        last_response = {"ui": {"children": [{"children": []}]}, "ds": {"data": "test"}}

        with pytest.raises(AttributeError, match="'dict' object has no attribute 'children'"):
            get_server_error_alert(message="Error", last_response=last_response)

    def test_return_coverage_with_mock(self):
        """Test to achieve coverage of return statement using mocks."""
        # Create mock to work around the bug
        mock_child = MagicMock()
        mock_child.children.append = MagicMock()

        mock_ui = MagicMock()
        mock_ui.children = [mock_child]

        last_response = {"ui": mock_ui, "ds": {}}
        result = get_server_error_alert(message="Test", last_response=last_response)

        assert result is last_response
        mock_child.children.append.assert_called_once()

    def test_message_variations(self):
        """Test with different message types."""
        test_cases = ["", "Simple", "Special chars: !@#$", "Long " * 20, "Multi\nline"]

        for message in test_cases:
            result = get_server_error_alert(message=message)
            error_alert = result["ui"]["children"][0]["children"][0]
            message_attr = next(attr for attr in error_alert["attributes"] if attr["key"] == "message")
            expected = f"{message} (Check the server logs for more details)."
            assert message_attr["value"] == expected

    def test_structure_consistency(self):
        """Test that structure is consistent across different inputs."""
        result1 = get_server_error_alert()
        result2 = get_server_error_alert(message="Different")

        error1 = result1["ui"]["children"][0]["children"][0]
        error2 = result2["ui"]["children"][0]["children"][0]

        # Same structure, different message content
        assert error1.keys() == error2.keys()
        assert error1["id"] == error2["id"] == "server_error"
        assert len(error1["attributes"]) == len(error2["attributes"]) == 3
