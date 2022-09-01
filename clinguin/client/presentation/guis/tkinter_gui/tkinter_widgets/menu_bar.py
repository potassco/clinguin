"""
This module features the MenuBar class.
"""
import tkinter as tk

from .root_cmp import *

class MenuBar(RootCmp):
    """
    The MenuBar is the class which resembles the menu-bar in tkinter. There must only be one in a clinguin ui file.
    """

    def _initWidget(self, elements):
        parent_widget = elements[self._parent].getWidget()
        menubar = tk.Menu(parent_widget)
        parent_widget.config(menu=menubar)

        return menubar

    def _addComponentToElements(self, elements):
        elements[str(self._id)] = self


