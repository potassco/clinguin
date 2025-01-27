"""
Module contains the menu bar section class.
"""

import tkinter as tk

from clinguin.utils.attribute_types import StringType

from ..tkinter_utils import AttributeNames
from .root_cmp import RootCmp


class MenuBarSection(RootCmp):
    """
    The menu bar section is a section of a menu bar
    (e.g. in the menu |main|contact|,
    where if one clicks on |contact|
    further the options |location|team|
    appear, a menu-bar-section would be |contact|,
    whereas |location| and |team| would be menu-bar-section-items.
    """

    def _init_element(self, elements):
        menubar_element = elements[self._parent].get_element()

        menubar_section = tk.Menu(menubar_element)

        return menubar_section

    @classmethod
    def _get_attributes(cls, attributes=None):
        if attributes is None:
            attributes = {}

        attributes[AttributeNames.label] = {
            "value": "default_label",
            "value_type": StringType,
        }

        return attributes

    def _set_sub_menu(self, elements):
        text = self._attributes[AttributeNames.label]["value"]

        menubar_element = elements[self._parent].get_element()
        menubar_element.add_cascade(label=text, menu=self._element)

    def _add_component_to_elements(self, elements):
        elements[str(self._id)] = self
