from tkinter import font
import tkinter as tk

from .root_cmp import RootCmp
from .standard_text_processing import StandardTextProcessing

from .attribute_names import AttributeNames
from .callback_names import CallbackNames


class Button(RootCmp):


    def _initWidget(self, elements):
        button = tk.Button(elements[str(self._parent)].getWidget())
        return button

    @classmethod
    def getAttributes(cls):
        attributes = {}
        # Label/Text
        attributes[AttributeNames.label] = {"value":""}
        # Color
        attributes[AttributeNames.backgroundcolor] = {"value":"white"}
        attributes[AttributeNames.foregroundcolor] = {"value":"black"}
        # Geom
        attributes[AttributeNames.width] = {"value":str(50)}
        attributes[AttributeNames.height] = {"value":str(50)}
        # Interactive-Attributes
        attributes[AttributeNames.onhover] = {"value":"false"}
        attributes[AttributeNames.onhover_background_color] = {"value":"white"}
        attributes[AttributeNames.onhover_foreground_color] = {"value":"black"}
        # Font
        attributes[AttributeNames.font_family] = {"value":"Helvetica"}
        attributes[AttributeNames.font_size] = {"value":str(12)}
        attributes[AttributeNames.font_weight] = {"value":"normal"}

        return attributes

    @classmethod
    def getCallbacks(cls):
        callbacks = {}

        callbacks[CallbackNames.click] = {"policy":None}

        return callbacks

    #----------------------------------------------------------------------------------------------
    #-----Attributes----
    #----------------------------------------------------------------------------------------------

    def _setLabelText(self, elements):
        text = self._attributes[AttributeNames.label]["value"]
        text = StandardTextProcessing.parseStringWithQuotes(text)
        self._widget.configure(text = text)

    def _setBackgroundColor(self, elements, key = AttributeNames.backgroundcolor):
        value = StandardTextProcessing.parseStringWithQuotes(self._attributes[key]["value"])
        self._widget.configure(background = value)

    def _setForegroundColor(self, elements, key = AttributeNames.foregroundcolor):
        value = StandardTextProcessing.parseStringWithQuotes(self._attributes[key]["value"])
        self._widget.configure(foreground = value)

    def _setWidth(self, elements):
        value = self._attributes[AttributeNames.width]["value"]
        if value.isdigit():
            self._widget.configure(width = int(value))
        else:
            self._logger.warn("For element " + self._id + " ,setWidth for width is not a digit: " + value)

    def _setHeight(self, elements):
        value = self._attributes[AttributeNames.height]["value"]
        if value.isdigit():
            self._widget.configure(height = int(value))
        else:
            self._logger.warn("For element " + self._id + " ,setHeight for height  is not a digit: " + value)
  
    def _setOnHover(self, elements): 
        on_hover = self._attributes[AttributeNames.onhover]["value"]
        on_hover_background_color = self._attributes[AttributeNames.onhover_background_color]["value"]
        on_hover_background_color = StandardTextProcessing.parseStringWithQuotes(on_hover_background_color)

        on_hover_foreground_color = self._attributes[AttributeNames.onhover_foreground_color]["value"]
        on_hover_foreground_color = StandardTextProcessing.parseStringWithQuotes(on_hover_foreground_color)

        if on_hover == "true":
            def enter(event):
                if on_hover_background_color != "":
                    self._setBackgroundColor(elements, key = AttributeNames.onhover_background_color)
                if on_hover_foreground_color != "":
                    self._setForegroundColor(elements, key = AttributeNames.onhover_foreground_color)

            def leave(event):
                self._setBackgroundColor(elements)
                self._setForegroundColor(elements)
    
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






