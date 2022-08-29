import tkinter as tk

from .root_cmp import *

class Container(RootCmp, LayoutFollower, LayoutController, ConfigureSize, ConfigureBorder):

    def _initWidget(self, elements):
        container = tk.Frame(elements[str(self._parent)].getWidget())
        return container

    @classmethod
    def _getAttributes(cls, attributes = None):
        if attributes is None:
            attributes = {}

        attributes[AttributeNames.backgroundcolor] = {"value":"white", "value_type" : ColorType, "description": "CUSTOM-BACKGROUND-COLOR-DESCRIPTION <- Now normal:" + AttributeNames.descriptions[AttributeNames.backgroundcolor]}
        # Interactive-Attributes
        attributes[AttributeNames.onhover] = {"value":False, "value_type" : BooleanType}
        attributes[AttributeNames.onhover_background_color] = {"value":"", "value_type" : ColorType}
        attributes[AttributeNames.onhover_border_color] = {"value":"", "value_type" : ColorType}

        return attributes

    @classmethod
    def _getCallbacks(cls, callbacks = None):
        if callbacks is None:
            callbacks = {}

        callbacks["click"] = {"policy":None, "policy_type" : SymbolType}

        return callbacks

    #----------------------------------------------------------------------------------------------
    #-----Attributes----
    #----------------------------------------------------------------------------------------------

    def _setBackgroundColor(self, elements, key = AttributeNames.backgroundcolor):
        value = self._attributes[key]["value"]
        self._widget.configure(background = value)
    def _setOnHover(self, elements): 
        on_hover = self._attributes[AttributeNames.onhover]["value"]
        on_hover_color = self._attributes[AttributeNames.onhover_background_color]["value"]
        on_hover_border_color = self._attributes[AttributeNames.onhover_border_color]["value"]

        if on_hover:
            def enter(event):
                if on_hover_color != "":
                    self._setBackgroundColor(elements, key = AttributeNames.onhover_background_color)
                if on_hover_border_color != "":
                    self._setBorderBackgroundColor(elements, key = AttributeNames.onhover_border_color)

            def leave(event):
                self._setBackgroundColor(elements, key = AttributeNames.backgroundcolor)
                self._setBorderBackgroundColor(elements, key = AttributeNames.border_color)
            
            self._widget.bind('<Enter>', enter)
            self._widget.bind('<Leave>', leave)
 
    #----------------------------------------------------------------------------------------------
    #-----Actions----
    #----------------------------------------------------------------------------------------------
       
    def _defineClickEvent(self, elements, key = CallbackNames.click):
        if self._callbacks[key] and self._callbacks[key]["policy"]:
            def dropdownmenuitemClick(event):
                self._base_engine.assume(self._callbacks[key]["policy"])

            self._widget.bind('<Button-1>', dropdownmenuitemClick)





