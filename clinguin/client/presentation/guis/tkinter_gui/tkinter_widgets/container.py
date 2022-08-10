import tkinter as tk

from .root_cmp import *

class Container(RootCmp, LayoutFollower, LayoutController):

    def _initWidget(self, elements):
        container = tk.Frame(elements[str(self._parent)].getWidget())
        return container

    @classmethod
    def _getAttributes(cls, attributes = None):
        if attributes == None:
            attributes = {}

        attributes[AttributeNames.backgroundcolor] = {"value":"white", "value_type" : ColorType, "description": "CUSTOM-BACKGROUND-COLOR-DESCRIPTION <- Now normal:" + AttributeNames.descriptions[AttributeNames.backgroundcolor]}
        attributes[AttributeNames.width] = {"value":-1, "value_type" : IntegerType}
        attributes[AttributeNames.height] = {"value":-1, "value_type" : IntegerType}
        attributes[AttributeNames.border_width] = {"value":0, "value_type" : IntegerType}
        attributes[AttributeNames.border_color] = {"value":"black", "value_type" : ColorType}

        # Interactive-Attributes
        attributes[AttributeNames.onhover] = {"value":False, "value_type" : BooleanType}
        attributes[AttributeNames.onhover_background_color] = {"value":"", "value_type" : ColorType}
        attributes[AttributeNames.onhover_border_color] = {"value":"", "value_type" : ColorType}

        return attributes

    @classmethod
    def getCallbacks(cls):
        callbacks = {}

        callbacks["click"] = {"policy":None, "policy_type" : SymbolType}

        return callbacks

    #----------------------------------------------------------------------------------------------
    #-----Attributes----
    #----------------------------------------------------------------------------------------------

    def _setBackgroundColor(self, elements, key = AttributeNames.backgroundcolor):
        value = self._attributes[key]["value"]
        self._widget.configure(background = value)

    def _setWidth(self, elements, key = AttributeNames.width):
        value = self._attributes[key]["value"]
        self._widget.configure(width = int(value))

    def _setHeight(self, elements, key = AttributeNames.height):
        value = self._attributes[key]["value"]
        self._widget.configure(height = int(value))

    def _setBorderWidth(self, elements, key = AttributeNames.border_width):
        value = self._attributes[key]["value"]
        if value > 0:
            # Not using borderwidth as one cannot set the color of the default border
            self._widget.configure(highlightthickness = int(value))
        elif value == 0:
            pass
        else:
            self._logger.warn("For element " + self._id + " ,setBorderwidth for " + key + " is lesser than 0: " + str(value))

    def _setBorderBackgroundColor(self, elements, key = AttributeNames.border_color):
        # Not using borderwidth as one cannot set the color of the default border
        value = self._attributes[key]["value"]
        self._widget.configure(highlightbackground = value, highlightcolor = value)

    def _setOnHover(self, elements): 
        on_hover = self._attributes[AttributeNames.onhover]["value"]
        on_hover_color = self._attributes[AttributeNames.onhover_background_color]["value"]
        on_hover_border_color = self._attributes[AttributeNames.onhover_border_color]["value"]

        if on_hover == True:
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





