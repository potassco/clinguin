import tkinter as tk

from clinguin.client.presentation.tkinter.root_cmp import RootCmp
from clinguin.client.presentation.tkinter.standard_text_processing import StandardTextProcessing

from clinguin.client.presentation.tkinter.attribute_names import AttributeNames
from clinguin.client.presentation.tkinter.callback_names import CallbackNames

class MenuBarSection(RootCmp):

    def _initWidget(self, elements):
        menubar_widget = elements[self._parent].getWidget()

        menubar_section = tk.Menu(menubar_widget)
        
        return menubar_section

    @classmethod
    def getAttributes(cls):
        attributes = {}

        attributes[AttributeNames.label] = {"value":"default_label"}

        return attributes


    def _setSubMenu(self, elements):
        value = self._attributes[AttributeNames.label]["value"]

        text = StandardTextProcessing.parseStringWithQuotes(value)

        menubar_widget = elements[self._parent].getWidget()
        menubar_widget.add_cascade(label=text, menu=self._widget)
        
    def _addComponentToElements(self, elements):
       
        elements[str(self._id)] = self



