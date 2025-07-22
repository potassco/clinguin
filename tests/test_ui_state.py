"""Test cases for UI State functionality using pytest."""

from pathlib import Path

import pytest

from clinguin.server.ui import UIState

TEST_DATA_DIR = Path(__file__).parent / "data"


def test_ui_state_str_method():
    """Test the __str__ method of UIState."""
    ui_state = UIState([str(TEST_DATA_DIR / "ui.lp")], "object(a).", [])
    ui_state.update_ui_state()

    str_result = str(ui_state)
    assert str_result.startswith("\nUI State:\n=========\n")
    assert len(str_result) > len("\nUI State:\n=========\n")


def test_ui_state_str_method_empty_factbase():
    """Test __str__ method when factbase is None."""
    ui_state = UIState([str(TEST_DATA_DIR / "ui.lp")], "", [])
    with pytest.raises(AttributeError):
        str(ui_state)


def test_ui_state_is_empty_property():
    """Test the is_empty property."""
    ui_state = UIState([str(TEST_DATA_DIR / "ui.lp")], "", [])
    assert ui_state.is_empty is True

    ui_state.update_ui_state()
    assert ui_state.is_empty is False


def test_get_attributes_for_element_id():
    """Test getting attributes for a specific element ID."""
    ui_state = UIState([str(TEST_DATA_DIR / "ui.lp")], "object(a).", [])
    ui_state.update_ui_state()

    elements = list(ui_state.get_elements())
    assert len(elements) > 0

    attributes = list(ui_state.get_attributes_for_element_id(elements[0].id))
    assert isinstance(attributes, list)

    for attr in attributes:
        assert attr.id == elements[0].id


def test_get_whens_for_element_id():
    """Test getting whens for a specific element ID."""
    ui_state = UIState([str(TEST_DATA_DIR / "ui.lp")], "object(a).", [])
    ui_state.update_ui_state()

    elements = list(ui_state.get_elements())
    whens = list(ui_state.get_whens_for_element_id(elements[0].id))
    assert isinstance(whens, list)

    for when in whens:
        assert when.id == elements[0].id


def test_replace_attribute():
    """Test replacing an attribute."""
    from clingo.symbol import String
    from clorm import Raw

    from clinguin.server.ui import Attribute

    ui_state = UIState([str(TEST_DATA_DIR / "ui.lp")], "object(a).", [])
    ui_state.update_ui_state()

    original_attributes = list(ui_state.get_attributes())
    if len(original_attributes) > 0:
        old_attribute = original_attributes[0]
        new_attribute = Attribute(
            Raw(old_attribute.id.symbol), Raw(old_attribute.key.symbol), Raw(String("new_test_value"))
        )

        ui_state.replace_attribute(old_attribute, new_attribute)
        updated_attributes = list(ui_state.get_attributes())

        assert len(updated_attributes) == len(original_attributes)
        assert old_attribute not in updated_attributes
        assert new_attribute in updated_attributes


def test_symbols_to_facts():
    """Test the symbols_to_facts class method."""
    from clingo import parse_term

    symbols = [parse_term("object(a)"), parse_term("object(b)")]
    result = UIState.symbols_to_facts(symbols)
    assert result == "object(a).\nobject(b)."

    assert UIState.symbols_to_facts([]) == ""
    assert UIState.symbols_to_facts([parse_term("single")]) == "single."


def test_set_fb_symbols():
    """Test the _set_fb_symbols method."""
    from clingo import parse_term

    ui_state = UIState([str(TEST_DATA_DIR / "ui.lp")], "", [])
    assert ui_state._factbase is None

    test_symbols = [
        parse_term("elem(w,window,root)"),
        parse_term('attr(w,title,"Test")'),
        parse_term('when(w,click,call,"op")'),
    ]

    ui_state._set_fb_symbols(test_symbols)
    assert ui_state._factbase is not None
    assert ui_state.is_empty is False

    assert len(list(ui_state.get_elements())) == 1
    assert len(list(ui_state.get_attributes())) == 1
    assert len(list(ui_state.get_whens())) == 1


def test_ui_control_nonexistent_file():
    """Test ui_control with non-existent file."""
    ui_state = UIState(["nonexistent.lp"], "", [])
    with pytest.raises(Exception, match="File nonexistent.lp does not exist"):
        ui_state.ui_control()


def test_ui_control_invalid_ui_file(tmp_path):
    """Test ui_control with invalid syntax file."""
    invalid_file = tmp_path / "invalid.lp"
    invalid_file.write_text("invalid syntax @#$%")

    ui_state = UIState([str(invalid_file)], "", [])
    with pytest.raises(Exception):
        ui_state.ui_control()


def test_ui_control_malformed_domain_state():
    """Test ui_control with malformed domain state."""
    ui_state = UIState([str(TEST_DATA_DIR / "ui.lp")], "invalid @#$%", [])
    with pytest.raises(RuntimeError):
        ui_state.ui_control()


def test_ui_control_successful():
    """Test successful ui_control execution."""
    ui_state = UIState([str(TEST_DATA_DIR / "ui.lp")], "object(a).", ["-c", "test=1"])
    uictl = ui_state.ui_control()
    assert uictl.__class__.__name__ == "Control"


def test_add_element_with_string_parameters():
    """Test add_element with string parameters."""
    ui_state = UIState([str(TEST_DATA_DIR / "ui.lp")], "object(a).", [])
    ui_state.update_ui_state()

    ui_state.add_element("test_elem", "button", "root")

    elements = list(ui_state.get_elements())
    added_elem = next((e for e in elements if str(e.id) == "test_elem"), None)
    assert added_elem is not None
    assert str(added_elem.type) == "button"


def test_add_attribute_with_string_and_int_parameters():
    """Test add_attribute with string and int parameters."""
    ui_state = UIState([str(TEST_DATA_DIR / "ui.lp")], "object(a).", [])
    ui_state.update_ui_state()

    ui_state.add_attribute("test_elem", "label", "Test")
    ui_state.add_attribute("test_elem", "width", 100)

    attributes = list(ui_state.get_attributes())
    string_attr = next((a for a in attributes if str(a.key) == "label"), None)
    int_attr = next((a for a in attributes if str(a.key) == "width"), None)

    assert string_attr is not None
    assert int_attr is not None


def test_add_attribute_direct():
    """Test add_attribute_direct method."""
    from clingo.symbol import Function, String
    from clorm import Raw

    from clinguin.server.ui import Attribute

    ui_state = UIState([str(TEST_DATA_DIR / "ui.lp")], "object(a).", [])
    ui_state.update_ui_state()

    initial_count = len(list(ui_state.get_attributes()))
    new_attribute = Attribute(
        Raw(Function("direct_elem", [])), Raw(Function("direct_key", [])), Raw(String("direct_value"))
    )

    ui_state.add_attribute_direct(new_attribute)
    assert len(list(ui_state.get_attributes())) == initial_count + 1


def test_replace_images_with_b64_no_image_attributes():
    """Test replace_images_with_b64 when no image attributes exist."""
    ui_state = UIState([str(TEST_DATA_DIR / "ui.lp")], "object(a).", [])
    ui_state.update_ui_state()

    ui_state.add_attribute("elem1", "title", "Test")
    initial_count = len(list(ui_state.get_attributes()))

    ui_state.replace_images_with_b64()
    assert len(list(ui_state.get_attributes())) == initial_count


def test_replace_images_with_b64_invalid_file():
    """Test replace_images_with_b64 with non-existent file."""
    ui_state = UIState([str(TEST_DATA_DIR / "ui.lp")], "object(a).", [])
    ui_state.update_ui_state()

    ui_state.add_attribute("elem1", "image", "nonexistent.png")
    initial_count = len(list(ui_state.get_attributes()))

    ui_state.replace_images_with_b64()
    assert len(list(ui_state.get_attributes())) == initial_count


def test_replace_images_with_b64_with_valid_image(tmp_path):
    """Test replace_images_with_b64 with valid image file."""
    image_file = tmp_path / "test.png"
    image_file.write_bytes(b"\x89PNG\r\n\x1a\n")

    ui_state = UIState([str(TEST_DATA_DIR / "ui.lp")], "object(a).", [])
    ui_state.update_ui_state()

    ui_state.add_attribute("elem1", "image", str(image_file))
    ui_state.replace_images_with_b64()

    image_attr = next((a for a in ui_state.get_attributes() if str(a.key) == "image"), None)
    assert image_attr is not None
    assert str(image_attr.value).strip('"') != str(image_file)


def test_replace_images_with_b64_custom_key():
    """Test replace_images_with_b64 with custom key."""
    ui_state = UIState([str(TEST_DATA_DIR / "ui.lp")], "object(a).", [])
    ui_state.update_ui_state()

    ui_state.add_attribute("elem1", "photo", "path.jpg")
    initial_count = len(list(ui_state.get_attributes()))

    ui_state.replace_images_with_b64(image_attribute_key="photo")
    assert len(list(ui_state.get_attributes())) == initial_count


def test_get_attributes_with_key_filter():
    """Test get_attributes with key filter."""
    from clingo.symbol import Function
    from clorm import Raw

    ui_state = UIState([str(TEST_DATA_DIR / "ui.lp")], "object(a).", [])
    ui_state.update_ui_state()

    ui_state.add_attribute("elem1", "title", "Test")

    key_filter = Raw(Function("title", []))
    filtered_attrs = list(ui_state.get_attributes(key=key_filter))
    assert isinstance(filtered_attrs, list)


def test_add_message_no_window():
    """Test add_message when no window exists."""
    from clingo import parse_term

    ui_state = UIState([str(TEST_DATA_DIR / "ui.lp")], "", [])
    test_symbols = [parse_term("elem(container1,container,root)")]
    ui_state._set_fb_symbols(test_symbols)

    with pytest.raises(ValueError, match="No window found"):
        ui_state.add_message("Title", "Message")


def test_update_ui_state_unsatisfiable(tmp_path):
    """Test update_ui_state with unsatisfiable encoding."""
    unsatisfiable_file = tmp_path / "unsat.lp"
    unsatisfiable_file.write_text("elem(w, window, root). :- elem(w, window, root).")

    ui_state = UIState([str(unsatisfiable_file)], "", [])
    with pytest.raises(RuntimeError, match="UNSATISFIABLE"):
        ui_state.update_ui_state()


def test_add_message_successful():
    """Test successful add_message execution."""
    ui_state = UIState([str(TEST_DATA_DIR / "ui.lp")], "object(a).", [])
    ui_state.update_ui_state()

    initial_count = len(list(ui_state.get_elements()))
    ui_state.add_message("Title", "Message", "warning")

    assert len(list(ui_state.get_elements())) == initial_count + 1
    message_elem = next((e for e in ui_state.get_elements() if str(e.type) == "message"), None)
    assert message_elem is not None


def test_add_element_with_non_string_parameters():
    """Test add_element with Function objects."""
    from clingo.symbol import Function

    ui_state = UIState([str(TEST_DATA_DIR / "ui.lp")], "object(a).", [])
    ui_state.update_ui_state()

    ui_state.add_element(Function("func_elem", []), Function("button", []), Function("root", []))

    added_elem = next((e for e in ui_state.get_elements() if str(e.id) == "func_elem"), None)
    assert added_elem is not None


def test_add_attribute_with_non_string_parameters():
    """Test add_attribute with Function/String/Number objects."""
    from clingo.symbol import Function, Number, String

    ui_state = UIState([str(TEST_DATA_DIR / "ui.lp")], "object(a).", [])
    ui_state.update_ui_state()

    ui_state.add_attribute(Function("func_elem", []), Function("func_key", []), String("func_value"))

    ui_state.add_attribute(Function("func_elem", []), Function("func_key2", []), Number(42))

    string_attr = next((a for a in ui_state.get_attributes() if str(a.key) == "func_key"), None)
    number_attr = next((a for a in ui_state.get_attributes() if str(a.key) == "func_key2"), None)

    assert string_attr is not None
    assert number_attr is not None
