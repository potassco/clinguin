from tkinter import font
import tkinter as tk

from .root_cmp import *

class Label(RootCmp):

    def _initWidget(self, elements):
        label = tk.Label(elements[str(self._parent)].getWidget())
        return label

    @classmethod
    def getAttributes(cls):
        attributes = {}

        attributes[AttributeNames.label] = {"value":"", "value_type" : StringType}
        attributes[AttributeNames.backgroundcolor] = {"value":"white", "value_type" : ColorType}
        attributes[AttributeNames.foregroundcolor] = {"value":"black", "value_type" : ColorType}
        attributes[AttributeNames.width] = {"value":50, "value_type" : IntegerType}
        attributes[AttributeNames.height] = {"value":50, "value_type" : IntegerType}
        # Interactive-Attributes
        attributes[AttributeNames.onhover] = {"value":False, "value_type" : BooleanType}
        attributes[AttributeNames.onhover_background_color] = {"value":"white", "value_type" : ColorType}
        attributes[AttributeNames.onhover_foreground_color] = {"value":"black", "value_type" : ColorType}

        attributes[AttributeNames.font_family] = {"value":"Helvetica", "value_type" : StringType}
        attributes[AttributeNames.font_size] = {"value":12, "value_type" : IntegerType}
        attributes[AttributeNames.font_weight] = {"value":"normal", "value_type" : StringType}

        return attributes

    @classmethod
    def getCallbacks(cls):
        callbacks = {}

        callbacks[CallbackNames.click] = {"policy":None, "policy_type": SymbolType}

        return callbacks

    #----------------------------------------------------------------------------------------------
    #-----Standard-Attributes----
    #----------------------------------------------------------------------------------------------

    def _setLabelText(self, elements, key = AttributeNames.label):
        text = self._attributes[key]["value"]
        self._widget.configure(text = text)

    def _setBackgroundColor(self, elements, key = AttributeNames.backgroundcolor):
        value = self._attributes[key]["value"]
        self._widget.configure(background = value)

    def _setForegroundColor(self, elements, key = AttributeNames.foregroundcolor):
        value = self._attributes[key]["value"]
        self._widget.configure(foreground = value)

    def _setWidth(self, elements, key = AttributeNames.width):
        value = self._attributes[key]["value"]
        self._widget.configure(width = int(value))

    def _setHeight(self, elements, key = AttributeNames.height):
        value = self._attributes[key]["value"]
        self._widget.configure(height = int(value))

    #----------------------------------------------------------------------------------------------
    #-----Special-Attributes----
    #----------------------------------------------------------------------------------------------

    def _setOnHover(self, elements): 
        on_hover = self._attributes[AttributeNames.onhover]["value"]
        on_hover_background_color = self._attributes[AttributeNames.onhover_background_color]["value"]

        on_hover_foreground_color = self._attributes[AttributeNames.onhover_foreground_color]["value"]

        if on_hover == True:
            def enter(event):
                if on_hover_background_color != "":
                    self._setBackgroundColor(elements, key = AttributeNames.onhover_background_color)
                if on_hover_foreground_color != "":
                    self._setForegroundColor(elements, key = AttributeNames.onhover_foreground_color)

            def leave(event):
                self._setBackgroundColor(elements, key = AttributeNames.backgroundcolor)
                self._setForegroundColor(elements, key= AttributeNames.foregroundcolor)
    
            self._widget.bind('<Enter>', enter)
            self._widget.bind('<Leave>', leave)

    def _setFont(self, elements):

        afont = font.Font(family=self._attributes[AttributeNames.font_family]["value"],
            size = int(self._attributes[AttributeNames.font_size]["value"]), weight = self._attributes[AttributeNames.font_weight]["value"])
        self._widget.configure(font=afont)


 
    #----------------------------------------------------------------------------------------------
    #-----Actions----
    #----------------------------------------------------------------------------------------------
       
    def _defineClickEvent(self, elements):
        key = CallbackNames.click
        if self._callbacks[key] and self._callbacks[key]["policy"]:
            def clickEvent(event):
                self._base_engine.postWithPolicy(self._callbacks[key]["policy"])

            self._widget.bind('<Button-1>', clickEvent)

    def _addComponentToElements(self, elements):
        self._widget.pack(expand=True)
        elements[str(self._id)] = self





