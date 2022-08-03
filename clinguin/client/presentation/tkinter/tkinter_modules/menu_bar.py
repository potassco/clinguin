import tkinter as tk

from .root_cmp import RootCmp

from .attribute_names import AttributeNames
from .callback_names import CallbackNames

class MenuBar(RootCmp):

    def _initWidget(self, elements):
        parent_widget = elements[self._parent].getWidget()
        menubar = tk.Menu(parent_widget)
        parent_widget.config(menu=menubar)

        return menubar

    def _addComponentToElements(self, elements):
        elements[str(self._id)] = self


