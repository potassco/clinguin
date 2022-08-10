import tkinter as tk

from .root_cmp import *

class Window(RootCmp, LayoutController):

    def _initWidget(self, elements):
        window = tk.Tk()
        window.title("Clinguin")

        return window

    @classmethod
    def _getAttributes(cls, attributes = None):
        if attributes == None:
            attributes = {}

        attributes[AttributeNames.backgroundcolor] = {"value":"white", "value_type" : ColorType}
        attributes[AttributeNames.width] = {"value":250, "value_type" : IntegerType}
        attributes[AttributeNames.height] = {"value":250, "value_type" : IntegerType}
        attributes[AttributeNames.resizable_x] = {"value":1, "value_type" : IntegerType}
        attributes[AttributeNames.resizable_y] = {"value":1, "value_type" : IntegerType}

        return attributes

    def _setBackgroundColor(self, elements, key = AttributeNames.backgroundcolor):
        value = self._attributes[key]["value"]
        self._widget.configure(background = value)

    def _setDimensions(self, elements):
        self._widget.geometry(str(self._attributes[AttributeNames.width]['value']) + 'x' +
            str(self._attributes[AttributeNames.height]['value']) + '+' +
            str(int(self._widget.winfo_screenwidth()/2 - int(self._attributes[AttributeNames.width]['value'])/2)) + '+' +
            str(int(self._widget.winfo_screenheight()/2 - int(self._attributes[AttributeNames.height]['value'])/2)))

    def _setResizable(self, elements):
        self._widget.resizable(self._attributes[AttributeNames.resizable_x]['value'],self._attributes[AttributeNames.resizable_y]['value'])
    def _addComponentToElements(self, elements):
        elements[str(self._id)] = self


