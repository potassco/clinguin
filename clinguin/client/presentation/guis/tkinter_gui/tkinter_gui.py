import tkinter as tk
import logging

from clinguin.show_gui_syntax_enum import ShowGuiSyntaxEnum
from clinguin.client import AbstractGui

from .tkinter_widgets import *
from .tkinter_utils import *


class TkinterGui(AbstractGui):

    def __init__(self, base_engine, args):
        super().__init__(base_engine, args)

        self.elements = {}
        self.first = True

    @classmethod
    def registerOptions(cls, parser):   
        parser.description = "This GUI is based on the Python-Tkinter package and uses tkinter widgets."
        return 

    @classmethod
    def availableSyntax(cls, show_lvl):
        def appendDict(description, _dict, type_name):

            for key in _dict.keys():
                description = description + "    |- " + key + "\n"
                if show_lvl == ShowGuiSyntaxEnum.FULL:
                    if "description" in _dict[key]:
                        # Specific has higher priority
                        description = description + "      |- Description: "
                        description = description + ": " + _dict[key]["description"]
                        description = description + "\n"
                    elif key in AttributeNames.descriptions:
                        # General lesser priority
                        description = description + "      |- Description: "
                        description = description + ": " + AttributeNames.descriptions[key]
                        description = description + "\n"
                    elif key in CallbackNames.descriptions:
                        description = description + "      |- Description: "
                        description = description + ": " + CallbackNames.descriptions[key]
                        description = description + "\n"

                    if type_name in _dict[key]:
                        description = description + "      |- Possible-Values: "
                        description = description + _dict[key][type_name].description() + "\n"

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
                description = appendDict(description, attributes, "value_type")
            
            callbacks = c.getCallbacks()
            if len(callbacks.keys()) > 0:               
                description = description + "  |- callbacks\n"
                description = appendDict(description, callbacks, "policy_type")
            description = description + "|--------------------------------\n"

        return description


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


    def dropdownMenu(self, id, parent, attributes, callbacks):
        menu = Dropdownmenu(self._args, id, parent, attributes, callbacks, self._base_engine)
        menu.addComponent(self.elements)

    def dropdownMenuItem(self, id, parent, attributes, callbacks):
        menu = DropdownmenuItem(self._args, id, parent, attributes, callbacks, self._base_engine)
        menu.addComponent(self.elements)

    def label(self, id, parent, attributes, callbacks):
        label = Label(self._args, id, parent, attributes, callbacks, self._base_engine)
        label.addComponent(self.elements)

    def button(self, id, parent, attributes, callbacks):
        button = Button(self._args, id, parent, attributes, callbacks, self._base_engine)
        button.addComponent(self.elements)

    def menuBar(self, id, parent, attributes, callbacks):
        menubar = MenuBar(self._args, id, parent, attributes, callbacks, self._base_engine)
        menubar.addComponent(self.elements)

    def menuBarSection(self, id, parent, attributes, callbacks):
        menubar = MenuBarSection(self._args, id, parent, attributes, callbacks, self._base_engine)
        menubar.addComponent(self.elements)

    def menuBarSectionItem(self, id, parent, attributes, callbacks):
        menubar = MenuBarSectionItem(self._args, id, parent, attributes, callbacks, self._base_engine)
        menubar.addComponent(self.elements)

    def message(self, id, parent, attributes, callbacks):
        message = Message(self._args, id, parent, attributes, callbacks, self._base_engine)
        message.addComponent(self.elements)

    def draw(self, id):
        self.first = False
        self.elements[id].getWidget().mainloop()
