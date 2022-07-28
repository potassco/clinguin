import tkinter as tk

from .window import Window
from .container import Container
from .dropdownmenu import Dropdownmenu
from .dropdownmenu_item import DropdownmenuItem

from clinguin.client.presentation.abstract_gui import AbstractGui


class Attribute:
    def __init__(self, id, key, value, action):
        self.id = id
        self.key = key
        self.value = value
        self.action = action


class TkinterGui(AbstractGui):

    def __init__(self, base_engine):
        self.elements = {}
        self._base_engine = base_engine

        self.first = True

    def window(self, id, parent, attributes, callbacks):
        #print("WINDOW: " + str(id) + "::" + str(parent))

        if self.first:
            window = Window(id, parent, attributes, callbacks, self._base_engine)
            window.addComponent(self.elements)
        else:
            keys = list(self.elements.keys()).copy()
            for key in keys:
                if str(key) == str(id):
                    continue

                self.elements[str(key)][0].pack_forget()
                del self.elements[str(key)]

    def container(self, id, parent, attributes, callbacks):
        container = Container(id, parent, attributes, callbacks, self._base_engine)
        container.addComponent(self.elements)


    def dropdownmenu(self, id, parent, attributes, callbacks):
        menu = Dropdownmenu(id, parent, attributes, callbacks, self._base_engine)
        menu.addComponent(self.elements)

    def dropdownmenuitem(self, id, parent, attributes, callbacks):
        menu = DropdownmenuItem(id, parent, attributes, callbacks, self._base_engine)
        menu.addComponent(self.elements)

    def draw(self, id):
        self.first = False
        self.elements[id][0].mainloop()
