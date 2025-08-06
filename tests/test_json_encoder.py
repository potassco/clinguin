"""
Test cases for the JsonEncoder class.
"""

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from clinguin.server.json_encoder import ElementDTO, JsonEncoder


def test_generate_hierarchy_undefined_parent_raises():
    """Test that an undefined parent raises an exception."""
    ui_state = SimpleNamespace()
    fake_elem = SimpleNamespace(id="a", parent="b", type="button")
    ui_state.get_elements = lambda: [fake_elem]

    with pytest.raises(Exception, match=r"Parent element \(ID: b\) undefined"):
        JsonEncoder._generate_hierarchy(ui_state, ElementDTO(id="root", type="root", parent="root"), {})


def test_generate_hierarchy_missing_element_info_raises():
    """Test that missing element info raises an exception."""
    ui_state = SimpleNamespace()
    e1 = SimpleNamespace(id="a", parent="root", type="box")
    ui_state.get_elements = lambda: [e1]
    ui_state.get_attributes_grouped = lambda: []
    ui_state.get_whens_grouped = lambda: []

    root = ElementDTO(id="root", type="root", parent="root")
    elements_dict = {"root": root}

    with patch("networkx.topological_sort", return_value=["missing_id", "a"]):
        with pytest.raises(Exception, match=r"ID 'missing_id'.*could not be found"):
            JsonEncoder._generate_hierarchy(ui_state, root, elements_dict)
