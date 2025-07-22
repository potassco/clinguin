import pytest

from clinguin.utils.text import parse_string_with_quotes


@pytest.mark.parametrize(
    "input_str, expected",
    [
        ('"Hello\\nWorld"', "Hello\nWorld"),  # Both quotes and escaped newline
        ('"Hello"', "Hello"),  # Quoted string without newline
        ('Hello"', "Hello"),  # Only ending quote
        ('"Hello', "Hello"),  # Only starting quote
        ("Hello", "Hello"),  # No quotes at all
        ("", ""),  # Empty string
        ('"\\n"', "\n"),  # Only escaped newline in quotes
    ],
)
def test_parse_string_with_quotes(input_str, expected):
    assert parse_string_with_quotes(input_str) == expected
