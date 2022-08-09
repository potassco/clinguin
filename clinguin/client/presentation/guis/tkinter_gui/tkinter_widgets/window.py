import tkinter as tk

from .root_cmp import RootCmp

from tkinter_gui.tkinter_utils.standard_text_processing import StandardTextProcessing
from tkinter_gui.tkinter_utils.attribute_names import AttributeNames
from tkinter_gui.tkinter_utils.callback_names import CallbackNames

class Window(RootCmp):

    def _initWidget(self, elements):
        window = tk.Tk()
        window.title("Clinguin")

        return window

    @classmethod
    def getAttributes(cls):
        attributes = {}

        attributes[AttributeNames.backgroundcolor] = {"value":"white"}
        attributes[AttributeNames.width] = {"value":str(250)}
        attributes[AttributeNames.height] = {"value":str(250)}
        attributes[AttributeNames.resizable_x] = {"value":str(1)}
        attributes[AttributeNames.resizable_y] = {"value":str(1)}
        attributes[AttributeNames.child_org] = {"value":"flex"}

        return attributes

    def _setBackgroundColor(self, elements, key = AttributeNames.backgroundcolor):
        value = StandardTextProcessing.parseStringWithQuotes(self._attributes[key]["value"])
        self._widget.configure(background = value)

    def _setDimensions(self, elements):
        self._widget.geometry(self._attributes[AttributeNames.width]['value'] + 'x' +
            self._attributes[AttributeNames.height]['value'] + '+' +
            str(int(self._widget.winfo_screenwidth()/2 - int(self._attributes[AttributeNames.width]['value'])/2)) + '+' +
            str(int(self._widget.winfo_screenheight()/2 - int(self._attributes[AttributeNames.height]['value'])/2)))

    def _setResizable(self, elements):
        self._widget.resizable(self._attributes[AttributeNames.resizable_x]['value'],self._attributes[AttributeNames.resizable_y]['value'])

    def _setChildOrg(self, elements):
        self._child_org = self._attributes[AttributeNames.child_org]["value"]

    def getChildOrg(self):
        return self._child_org

    def _addComponentToElements(self, elements):
        elements[str(self._id)] = self


