import tkinter as tk
import logging

from clinguin.client.presentation.tkinter.window import Window
from clinguin.client.presentation.tkinter.container import Container
from clinguin.client.presentation.tkinter.dropdownmenu import Dropdownmenu
from clinguin.client.presentation.tkinter.dropdownmenu_item import DropdownmenuItem
from clinguin.client.presentation.tkinter.label import Label
from clinguin.client.presentation.tkinter.button import Button

from clinguin.client.presentation.tkinter.menu_bar import MenuBar
from clinguin.client.presentation.tkinter.menu_bar_section import MenuBarSection
from clinguin.client.presentation.tkinter.menu_bar_section_item import MenuBarSectionItem

from clinguin.client.presentation.abstract_gui import AbstractGui

class TkinterGui(AbstractGui):

    def __init__(self, base_engine, args):
        super().__init__(base_engine, args)

        self.elements = {}
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
                
                if str(key) in self.elements:
                    self.elements[str(key)].forgetChildren(self.elements)
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

    def menubar(self, id, parent, attributes, callbacks):
        menubar = MenuBar(self._args, id, parent, attributes, callbacks, self._base_engine)
        menubar.addComponent(self.elements)

    def menubarsection(self, id, parent, attributes, callbacks):
        menubar = MenuBarSection(self._args, id, parent, attributes, callbacks, self._base_engine)
        menubar.addComponent(self.elements)

    def menubarsectionitem(self, id, parent, attributes, callbacks):
        menubar = MenuBarSectionItem(self._args, id, parent, attributes, callbacks, self._base_engine)
        menubar.addComponent(self.elements)

    def draw(self, id):
        self.first = False
        self.elements[id].getWidget().mainloop()
