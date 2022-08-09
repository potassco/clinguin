import tkinter as tk

from .root_cmp import RootCmp

from tkinter_gui.tkinter_utils.attribute_names import AttributeNames
from tkinter_gui.tkinter_utils.callback_names import CallbackNames

class MenuBar(RootCmp):

    def _initWidget(self, elements):
        parent_widget = elements[self._parent].getWidget()
        menubar = tk.Menu(parent_widget)
        parent_widget.config(menu=menubar)

        return menubar

    def _addComponentToElements(self, elements):
        elements[str(self._id)] = self


