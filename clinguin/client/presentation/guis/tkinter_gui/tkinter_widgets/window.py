import tkinter as tk

from .root_cmp import *

class Window(RootCmp):

    def _initWidget(self, elements):
        window = tk.Tk()
        window.title("Clinguin")

        return window

    @classmethod
    def getAttributes(cls):
        attributes = {}

        attributes[AttributeNames.backgroundcolor] = {"value":"white", "value_type" : ColorType}
        attributes[AttributeNames.width] = {"value":250, "value_type" : IntegerType}
        attributes[AttributeNames.height] = {"value":250, "value_type" : IntegerType}
        attributes[AttributeNames.resizable_x] = {"value":1, "value_type" : IntegerType}
        attributes[AttributeNames.resizable_y] = {"value":1, "value_type" : IntegerType}
        attributes[AttributeNames.child_layout] = {"value": ChildLayoutType.FLEX, "value_type" : ChildLayoutType}

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

    def _setChildOrg(self, elements):
        self._child_layout = self._attributes[AttributeNames.child_layout]["value"]

    def getChildOrg(self):
        return self._child_layout

    def _addComponentToElements(self, elements):
        elements[str(self._id)] = self


