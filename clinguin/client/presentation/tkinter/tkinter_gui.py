import tkinter as tk
import logging

from .window import Window
from .container import Container
from .dropdownmenu import Dropdownmenu
from .dropdownmenu_item import DropdownmenuItem
from .label import Label
from .button import Button

from clinguin.client.presentation.abstract_gui import AbstractGui

class TkinterGui(AbstractGui):

    def __init__(self, base_engine, args):
        self._logger = logging.getLogger(args.log_args['name'])
        self._args = args

        self.elements = {}
        self._base_engine = base_engine

        self.first = True

    def window(self, id, parent, attributes, callbacks):

        if self.first:
            window = Window(self._args, id, parent, attributes, callbacks, self._base_engine)
            window.addComponent(self.elements)
        else:
            keys = list(self.elements.keys()).copy()
            for key in keys:
                if str(key) == str(id):
                    continue

                self.elements[str(key)][0].pack_forget()
                del self.elements[str(key)]

    def container(self, id, parent, attributes, callbacks):
        container = Container(self._args, id, parent, attributes, callbacks, self._base_engine)
        container.addComponent(self.elements)


    def dropdownmenu(self, id, parent, attributes, callbacks):
        menu = Dropdownmenu(self._args, id, parent, attributes, callbacks, self._base_engine)
        menu.addComponent(self.elements)

    def dropdownmenuitem(self, id, parent, attributes, callbacks):
        menu = DropdownmenuItem(self._args, id, parent, attributes, callbacks, self._base_engine)
        menu.addComponent(self.elements)

    def label(self, id, parent, attributes, callbacks):
        label = Label(self._args, id, parent, attributes, callbacks, self._base_engine)
        label.addComponent(self.elements)

    def button(self, id, parent, attributes, callbacks):
        button = Button(self._args, id, parent, attributes, callbacks, self._base_engine)
        button.addComponent(self.elements)

    def draw(self, id):
        self.first = False
        self.elements[id][0].mainloop()
