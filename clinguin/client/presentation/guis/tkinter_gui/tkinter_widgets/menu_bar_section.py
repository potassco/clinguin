"""
Module contains the menu bar section class.
"""
import tkinter as tk

from .root_cmp import *

class MenuBarSection(RootCmp):
    """
    The menu bar section is a section of a menu bar (e.g. in the menu \|main\|contact\|, where if one clicks on \|contact\| further the options \|location\|team\| appear, a menu-bar-section would be \|contact\|, whereas \|location\| and \|team\| would be menu-bar-section-items.
    """

    def _initWidget(self, elements):
        menubar_widget = elements[self._parent].getWidget()

        menubar_section = tk.Menu(menubar_widget)
        
        return menubar_section

    @classmethod
    def _getAttributes(cls, attributes = None):
        if attributes is None:
            attributes = {}

        attributes[AttributeNames.label] = {"value":"default_label", "value_type" : StringType}

        return attributes


    def _setSubMenu(self, elements):
        text = self._attributes[AttributeNames.label]["value"]

        menubar_widget = elements[self._parent].getWidget()
        menubar_widget.add_cascade(label=text, menu=self._widget)
        
    def _addComponentToElements(self, elements):
       
        elements[str(self._id)] = self



