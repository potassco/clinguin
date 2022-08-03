
import tkinter as tk

from .root_cmp import RootCmp
from .standard_text_processing import StandardTextProcessing

from .attribute_names import AttributeNames
from .callback_names import CallbackNames


class Dropdownmenu(RootCmp):

    def _initWidget(self, elements):
        self._variable = tk.StringVar()
        items = []
        menu = tk.OptionMenu(elements[self._parent].getWidget(), self._variable, "", *items)

        return menu

    def getVariable(self):
        return self._variable

    @classmethod
    def getAttributes(cls):
        attributes = {}

        attributes[AttributeNames.backgroundcolor] = {"value":"white"}
        attributes[AttributeNames.foregroundcolor] = {"value":"black"}
        # Interactive-Attributes
        attributes[AttributeNames.onhover] = {"value":"false"}
        attributes[AttributeNames.onhover_background_color] = {"value":"white"}
        attributes[AttributeNames.onhover_foreground_color] = {"value":"black"}
        
        attributes[AttributeNames.selected] = {"value":""}
 
        return attributes

    def _setBackgroundColor(self, elements, key = AttributeNames.backgroundcolor):
        value = self._attributes[key]["value"]
        value = StandardTextProcessing.parseStringWithQuotes(value)
        
        self._widget.config(bg= value, activebackground=value)
        self._widget["menu"].config(bg=value, activebackground=value)

    def _setForegroundColor(self, elements, key = AttributeNames.foregroundcolor):
        value = self._attributes[key]["value"]
        value = StandardTextProcessing.parseStringWithQuotes(value)

        self._widget.config(fg=value, activeforeground=value)
        self._widget["menu"].config(fg=value, activeforeground=value)

    def _setOnHover(self, elements): 
        on_hover = self._attributes[AttributeNames.onhover]["value"]

        on_hover_background_color = self._attributes[AttributeNames.onhover_background_color]["value"]
        on_hover_background_color = StandardTextProcessing.parseStringWithQuotes(on_hover_background_color)

        on_hover_foreground_color = self._attributes[AttributeNames.onhover_foreground_color]["value"]
        on_hover_foreground_color = StandardTextProcessing.parseStringWithQuotes(on_hover_foreground_color)

        if on_hover == "true":
            self._widget.config(activebackground=on_hover_background_color, activeforeground=on_hover_foreground_color)
            self._widget["menu"].config(activebackground=on_hover_background_color, activeforeground=on_hover_foreground_color)

    def _setSelected(self, elements):
        if self._attributes[AttributeNames.selected]['value'] != "":
            self._variable.set(self._attributes[AttributeNames.selected]['value'])

    def _addComponentToElements(self, elements):
        self._widget.pack(expand=True)
        elements[str(self._id)] = self





