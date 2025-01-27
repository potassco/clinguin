"""
This module features the MenuBar class.
"""

import tkinter as tk

from .root_cmp import RootCmp


class MenuBar(RootCmp):
    """
    The MenuBar is the class which resembles the menu-bar in tkinter. There must only be one in a clinguin ui file.
    """

    def _init_element(self, elements):
        parent_element = elements[self._parent].get_element()
        menubar = tk.Menu(parent_element)
        parent_element.config(menu=menubar)

        return menubar

    def _add_component_to_elements(self, elements):
        elements[str(self._id)] = self
