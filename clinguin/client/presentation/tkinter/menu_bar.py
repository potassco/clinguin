import tkinter as tk

from clinguin.client.presentation.tkinter.root_cmp import RootCmp

class MenuBar(RootCmp):

    def _defineComponent(self, elements):
        parent_widget = elements[self._parent].getWidget()
        menubar = tk.Menu(parent_widget)
        parent_widget.config(menu=menubar)

        return menubar

    def _addComponentToElements(self, elements):
        elements[str(self._id)] = self


