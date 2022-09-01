"""
This module contains the Dropdownmenu class.
"""
import tkinter as tk

from .root_cmp import *

class Dropdownmenu(RootCmp, LayoutFollower, ConfigureSize):
    """
    The dropdownmenu is the master component for a dropdownmenu, i.e. dropdownmenu-items must be children of it. For available attributes see syntax definition. Implementation wise it is similarly implemented as the Label and Button - to make it work for layouting, the actual dropdownmenu is hidden and the widget is actually a tkinter frame (therefore self._widget is a frame, whereas self._menu is the dropdownmenu).
    """
    def __init__(self, args, id, parent, attributes, callbacks, base_engine):
        super().__init__(args, id, parent, attributes, callbacks, base_engine)
        
        self._menu = None
        self._variable = None


    def _initWidget(self, elements):

        option_menu_frame = tk.Frame(elements[str(self._parent)].getWidget())

        self._variable = tk.StringVar()
        items = []
        menu = tk.OptionMenu(option_menu_frame, self._variable, "", *items)

        self._menu = menu

        return option_menu_frame

    def getVariable(self):
        return self._variable

    @classmethod
    def _getAttributes(cls, attributes = None):
        if attributes is None:
            attributes = {}

        attributes[AttributeNames.backgroundcolor] = {"value":"white", "value_type" : ColorType}
        attributes[AttributeNames.foregroundcolor] = {"value":"black", "value_type" : ColorType}
        # Interactive-Attributes
        attributes[AttributeNames.onhover] = {"value":False, "value_type": BooleanType}
        attributes[AttributeNames.onhover_background_color] = {"value":"white", "value_type" : ColorType}
        attributes[AttributeNames.onhover_foreground_color] = {"value":"black", "value_type" : ColorType}
        
        attributes[AttributeNames.selected] = {"value":"", "value_type" : StringType}
 
        return attributes

    def _setBackgroundColor(self, elements, key = AttributeNames.backgroundcolor):
        value = self._attributes[key]["value"]
        
        self._menu.config(bg= value, activebackground=value)
        self._menu["menu"].config(bg=value, activebackground=value)

    def _setForegroundColor(self, elements, key = AttributeNames.foregroundcolor):
        value = self._attributes[key]["value"]

        self._menu.config(fg=value, activeforeground=value)
        self._menu["menu"].config(fg=value, activeforeground=value)

    def _setOnHover(self, elements): 
        on_hover = self._attributes[AttributeNames.onhover]["value"]

        on_hover_background_color = self._attributes[AttributeNames.onhover_background_color]["value"]

        on_hover_foreground_color = self._attributes[AttributeNames.onhover_foreground_color]["value"]

        if on_hover == "true":
            self._menu.config(activebackground=on_hover_background_color, activeforeground=on_hover_foreground_color)
            self._menu["menu"].config(activebackground=on_hover_background_color, activeforeground=on_hover_foreground_color)

    def _setSelected(self, elements):
        if self._attributes[AttributeNames.selected]['value'] != "":
            self._variable.set(self._attributes[AttributeNames.selected]['value'])

    def getMenu(self):
        return self._menu

    def _addComponentToElements(self, elements):
        self._menu.pack(expand=True, fill='both')

        elements[str(self._id)] = self





