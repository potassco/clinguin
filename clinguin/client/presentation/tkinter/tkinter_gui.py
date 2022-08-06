import tkinter as tk
import logging

from clinguin.client.presentation.abstract_gui import AbstractGui

from tkinter_modules.window import Window
from tkinter_modules.container import Container
from tkinter_modules.dropdownmenu import Dropdownmenu
from tkinter_modules.dropdownmenu_item import DropdownmenuItem
from tkinter_modules.label import Label
from tkinter_modules.button import Button

from tkinter_modules.menu_bar import MenuBar
from tkinter_modules.menu_bar_section import MenuBarSection
from tkinter_modules.menu_bar_section_item import MenuBarSectionItem
from tkinter_modules.message import Message

from tkinter_modules.attribute_names import AttributeNames
from tkinter_modules.callback_names import CallbackNames

class TkinterGui(AbstractGui):

    def __init__(self, base_engine, args):
        super().__init__(base_engine, args)

        self.elements = {}
        self.first = True

    @classmethod
    def registerOptions(cls, parser):   
        def appendDict(description, _dict):
            for key in _dict.keys():
                description = description + "    |- " + key
                if "description" in _dict[key]:
                    # Specific has higher priority
                    description = description + ": " + _dict[key]["description"]
                elif key in AttributeNames.descriptions:
                    # General lesser priority
                    description = description + ": " + AttributeNames.descriptions[key]
                elif key in CallbackNames.descriptions:
                    description = description + ": " + CallbackNames.descriptions[key]
                description = description + "\n"

            return description

        description = "Here one finds the supported attributes and callbacks of the TkinterGui and further a definition of the syntax:\n" +\
            "There are three syntax elements:\n\n" +\
            "element(<ID>, <TYPE>, <PARENT>) : To define an element\n" +\
            "attribute(<ID>, <KEY>, <VALUE>) : To define an attribute for an element (the ID is the ID of the corresponding element)\n" +\
            "callback(<ID>, <ACTION>, <POLICY>) : To define a callback for an element (the ID is the ID of the corresponding element)\n\n" +\
            "The following list shows for each <TYPE> the possible attributes and callbacks:\n" 

        class_list = [Window, Container, Label, Button, Dropdownmenu, DropdownmenuItem, MenuBar, MenuBarSection, MenuBarSectionItem]

        description = description + "|--------------------------------\n"
        for c in class_list:
            description = description + "|- " + c.__name__ + "\n"
            
            attributes = c.getAttributes()
            if len(attributes.keys()) > 0:
                description = description + "  |- attributes\n"
                description = appendDict(description, attributes)
            
            callbacks = c.getCallbacks()
            if len(callbacks.keys()) > 0:               
                description = description + "  |- callbacks\n"
                description = appendDict(description, callbacks)
            description = description + "|--------------------------------\n"

        parser.description = description

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

    def message(self, id, parent, attributes, callbacks):
        message = Message(self._args, id, parent, attributes, callbacks, self._base_engine)
        message.addComponent(self.elements)

    def draw(self, id):
        self.first = False
        self.elements[id].getWidget().mainloop()
