"""
Test ClinguinContext class with pytest.
"""

from unittest.mock import MagicMock, patch

import pytest
from clingo.symbol import Function, Number, String, Symbol, SymbolType

from clinguin.server.ui.clinguin_context import ClinguinContext


def test_concat_basic_strings():
    """Test concatenating basic string arguments"""
    context = ClinguinContext()
    result = context.concat("Hello", " ", "World")
    assert isinstance(result, Symbol)
    assert result.type == SymbolType.String
    assert result.string == "Hello World"


def test_concat_with_quotes():
    """Test concatenating strings with quotes that should be stripped"""
    context = ClinguinContext()
    result = context.concat('"Test "', '"1"')
    assert isinstance(result, Symbol)
    assert result.type == SymbolType.String
    assert result.string == "Test 1"


def test_concat_mixed_types():
    """Test concatenating different clingo symbol types"""
    context = ClinguinContext()
    string_arg = String("Test ")
    number_arg = Number(1)
    result = context.concat(string_arg, number_arg)
    assert isinstance(result, Symbol)
    assert result.type == SymbolType.String
    assert result.string == "Test 1"


def test_concat_single_argument():
    """Test concatenating a single argument"""
    context = ClinguinContext()
    result = context.concat("Hello")
    assert isinstance(result, Symbol)
    assert result.type == SymbolType.String
    assert result.string == "Hello"


def test_concat_empty_arguments():
    """Test concatenating with no arguments"""
    context = ClinguinContext()
    result = context.concat()
    assert isinstance(result, Symbol)
    assert result.type == SymbolType.String
    assert result.string == ""


def test_concat_function_symbols():
    """Test concatenating function symbols"""
    context = ClinguinContext()
    func_arg = Function("test", [Number(1)])
    result = context.concat("Value: ", func_arg)
    assert isinstance(result, Symbol)
    assert result.type == SymbolType.String
    assert result.string == "Value: test(1)"


def test_concat_preserves_internal_quotes():
    """Test that internal quotes are preserved while outer quotes are stripped"""
    context = ClinguinContext()
    result = context.concat('"He said "hello""')
    assert isinstance(result, Symbol)
    assert result.type == SymbolType.String
    assert result.string == 'He said "hello'


def test_concat_empty_strings():
    """Test concatenating empty strings"""
    context = ClinguinContext()
    result = context.concat("", "test", "")
    assert isinstance(result, Symbol)
    assert result.type == SymbolType.String
    assert result.string == "test"


def test_format_single_tuple_argument():
    """Test formatting with a single tuple argument (should unpack tuple arguments)"""
    context = ClinguinContext()
    tuple_arg = Function("", [String("World"), Number(42)])
    format_string = String("Hello {} and {}")

    result = context.format(format_string, tuple_arg)
    assert isinstance(result, Symbol)
    assert result.type == SymbolType.String
    assert result.string == "Hello World and 42"


def test_format_multiple_arguments():
    """Test formatting with multiple arguments (should use args directly)"""
    context = ClinguinContext()
    format_string = String("Hello {} and {}")

    result = context.format(format_string, String("World"), Number(42))
    assert isinstance(result, Symbol)
    assert result.type == SymbolType.String
    assert result.string == "Hello World and 42"


def test_format_single_non_tuple_argument():
    """Test formatting with a single non-tuple argument (should use args directly)"""
    context = ClinguinContext()
    format_string = String("Hello {}")

    result = context.format(format_string, String("World"))
    assert isinstance(result, Symbol)
    assert result.type == SymbolType.String
    assert result.string == "Hello World"


def test_format_single_function_with_name():
    """Test formatting with a single named function (should use args directly, not unpack)"""
    context = ClinguinContext()
    format_string = String("Function: {}")
    named_function = Function("test", [Number(1), Number(2)])

    result = context.format(format_string, named_function)
    assert isinstance(result, Symbol)
    assert result.type == SymbolType.String
    assert result.string == "Function: test(1,2)"


def test_format_with_quotes_stripped():
    """Test that quotes are stripped from arguments before formatting"""
    context = ClinguinContext()
    format_string = String("Say {}")

    result = context.format(format_string, String("hello"))
    assert isinstance(result, Symbol)
    assert result.type == SymbolType.String
    assert result.string == "Say hello"


def test_format_empty_tuple():
    """Test formatting with an empty tuple"""
    context = ClinguinContext()
    empty_tuple = Function("", [])
    format_string = String("No arguments")

    result = context.format(format_string, empty_tuple)
    assert isinstance(result, Symbol)
    assert result.type == SymbolType.String
    assert result.string == "No arguments"


def test_format_positional_indexing():
    """Test formatting with positional indexes"""
    context = ClinguinContext()
    format_string = String("{1} comes before {0}")

    result = context.format(format_string, String("second"), String("first"))
    assert isinstance(result, Symbol)
    assert result.type == SymbolType.String
    assert result.string == "first comes before second"


def test_upper_basic_string():
    """Test basic uppercase conversion"""
    context = ClinguinContext()
    result = context.upper("hello world")
    assert isinstance(result, Symbol)
    assert result.type == SymbolType.String
    assert result.string == "HELLO WORLD"


def test_upper_with_quotes():
    """Test uppercase conversion with quotes that should be stripped"""
    context = ClinguinContext()
    result = context.upper('"semester_1"')
    assert isinstance(result, Symbol)
    assert result.type == SymbolType.String
    assert result.string == "SEMESTER_1"


def test_upper_clingo_number():
    """Test uppercase conversion with clingo Number object"""
    context = ClinguinContext()
    number_arg = Number(42)
    result = context.upper(number_arg)
    assert isinstance(result, Symbol)
    assert result.type == SymbolType.String
    assert result.string == "42"


def test_upper_clingo_function():
    """Test uppercase conversion with clingo Function object"""
    context = ClinguinContext()
    func_arg = Function("test", [Number(1)])
    result = context.upper(func_arg)
    assert isinstance(result, Symbol)
    assert result.type == SymbolType.String
    assert result.string == "TEST(1)"


def test_upper_empty_string():
    """Test uppercase conversion with empty string"""
    context = ClinguinContext()
    result = context.upper("")
    assert isinstance(result, Symbol)
    assert result.type == SymbolType.String
    assert result.string == ""


def test_getattr_successful_lookup():
    """Test successful attribute lookup from __main__"""
    context = ClinguinContext()

    mock_main = MagicMock()
    mock_main.test_function = lambda x: x * 2

    with patch.dict("sys.modules", {"__main__": mock_main}):
        result = context.test_function
        assert result == mock_main.test_function


def test_getattr_missing_attribute():
    """Test AttributeError when attribute doesn't exist in __main__"""
    context = ClinguinContext()

    class MockMainModule:
        pass

    mock_main = MockMainModule()

    with patch.dict("sys.modules", {"__main__": mock_main}):
        with pytest.raises(AttributeError):
            _ = context.nonexistent_attr


def test_getattr_existing_context_attribute():
    """Test that existing ClinguinContext methods are not affected by __getattr__"""
    context = ClinguinContext()

    assert hasattr(context, "concat")
    assert hasattr(context, "format")
    assert hasattr(context, "stringify")
    assert hasattr(context, "upper")

    result = context.concat("hello", " world")
    assert result.string == "hello world"


def test_stringify_with_capitalize_true():
    """Test stringify with capitalize=True (covers the missing line)"""
    context = ClinguinContext()
    result = context.stringify("semester_1", capitalize=True)
    assert isinstance(result, Symbol)
    assert result.type == SymbolType.String
    assert result.string == "Semester 1"


def test_stringify_with_capitalize_false():
    """Test stringify with capitalize=False (default)"""
    context = ClinguinContext()
    result = context.stringify("semester_1", capitalize=False)
    assert isinstance(result, Symbol)
    assert result.type == SymbolType.String
    assert result.string == "semester 1"


def test_stringify_capitalize_with_quotes():
    """Test stringify with quotes and capitalize=True"""
    context = ClinguinContext()
    result = context.stringify('"hello_world"', capitalize=True)
    assert isinstance(result, Symbol)
    assert result.type == SymbolType.String
    assert result.string == "Hello world"


def test_stringify_capitalize_with_underscores():
    """Test stringify with multiple underscores and capitalize=True"""
    context = ClinguinContext()
    result = context.stringify("my_test_value", capitalize=True)
    assert isinstance(result, Symbol)
    assert result.type == SymbolType.String
    assert result.string == "My test value"


def test_stringify_capitalize_clingo_objects():
    """Test stringify with clingo objects and capitalize=True"""
    context = ClinguinContext()

    string_arg = String("test_value")
    result = context.stringify(string_arg, capitalize=True)
    assert isinstance(result, Symbol)
    assert result.type == SymbolType.String
    assert result.string == "Test value"

    func_arg = Function("my_function", [])
    result = context.stringify(func_arg, capitalize=True)
    assert isinstance(result, Symbol)
    assert result.type == SymbolType.String
    assert result.string == "My function"
