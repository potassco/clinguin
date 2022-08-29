import tkinter as tk

from .root_cmp import *

class Window(RootCmp, LayoutController):

    def _initWidget(self, elements):
        window = tk.Tk()
        window.title("Clinguin")

        return window

    @classmethod
    def _getAttributes(cls, attributes = None):
        if attributes is None:
            attributes = {}

        attributes[AttributeNames.backgroundcolor] = {"value":"white", "value_type" : ColorType}
        attributes[AttributeNames.width] = {"value":0, "value_type" : IntegerType}
        attributes[AttributeNames.height] = {"value":0, "value_type" : IntegerType}
        attributes[AttributeNames.pos_x] = {"value":-1, "value_type": IntegerType}
        attributes[AttributeNames.pos_y] = {"value":-1, "value_type": IntegerType}
        attributes[AttributeNames.resizable_x] = {"value":1, "value_type" : IntegerType}
        attributes[AttributeNames.resizable_y] = {"value":1, "value_type" : IntegerType}

        return attributes

    def _setBackgroundColor(self, elements, key = AttributeNames.backgroundcolor):
        value = self._attributes[key]["value"]
        self._widget.configure(background = value)

    def _setDimensions(self, elements):
        width = self._attributes[AttributeNames.width]["value"]
        height = self._attributes[AttributeNames.height]["value"]

        pos_x = self._attributes[AttributeNames.pos_x]["value"]
        pos_y = self._attributes[AttributeNames.pos_y]["value"]

        if height > 0 and width > 0:
            child_layout_value = self._attributes[AttributeNames.child_layout]["value"]

            if child_layout_value in (ChildLayoutType.FLEX, ChildLayoutType.RELSTATIC, ChildLayoutType.ABSSTATIC):
                self._widget.pack_propagate(0)
            elif child_layout_value == ChildLayoutType.GRID:
                self._widget.grid_propagate(0)
        
            if pos_x < 0:
                pos_x = int((int(self._widget.winfo_screenwidth()) - int(width)) / 2)
            if pos_y < 0:
                pos_y = int((int(self._widget.winfo_screenheight()) - int(height))/2)
            
            self._widget.geometry(str(width) + 'x' +
                str(height) + '+' +
                str(pos_x) + '+' +
                str(pos_y))

        elif (height > 0 and width <= 0) or (height <= 0 and width > 0):
            self._logger.warning("For the tkinter window one must set both height and width to positive values (not just one).")

    def _setResizable(self, elements):
        self._widget.resizable(self._attributes[AttributeNames.resizable_x]['value'],self._attributes[AttributeNames.resizable_y]['value'])
    def _addComponentToElements(self, elements):
        elements[str(self._id)] = self


