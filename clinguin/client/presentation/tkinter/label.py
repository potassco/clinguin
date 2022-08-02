from tkinter import font
import tkinter as tk

from clinguin.client.presentation.tkinter.root_cmp import RootCmp
from clinguin.client.presentation.tkinter.standard_text_processing import StandardTextProcessing

from clinguin.client.presentation.tkinter.attribute_names import AttributeNames
from clinguin.client.presentation.tkinter.callback_names import CallbackNames

class Label(RootCmp):

    def _initWidget(self, elements):
        label = tk.Label(elements[str(self._parent)].getWidget())
        return label

    @classmethod
    def getAttributes(cls):
        attributes = {}

        attributes[AttributeNames.label] = {"value":""}
        attributes[AttributeNames.backgroundcolor] = {"value":"white"}
        attributes[AttributeNames.foregroundcolor] = {"value":"black"}
        attributes[AttributeNames.width] = {"value":str(50)}
        attributes[AttributeNames.height] = {"value":str(50)}
        # Interactive-Attributes
        attributes[AttributeNames.onhover] = {"value":"false"}
        attributes[AttributeNames.onhover_background_color] = {"value":"white"}
        attributes[AttributeNames.onhover_foreground_color] = {"value":"black"}

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
    #-----Standard-Attributes----
    #----------------------------------------------------------------------------------------------

    def _setLabelText(self, elements, key = AttributeNames.label):
        text = StandardTextProcessing.parseStringWithQuotes(self._attributes[key]["value"])
        self._widget.configure(text = text)

    def _setBackgroundColor(self, elements, key = AttributeNames.backgroundcolor):
        value = StandardTextProcessing.parseStringWithQuotes(self._attributes[key]["value"])
        self._widget.configure(background = value)

    def _setForegroundColor(self, elements, key = AttributeNames.foregroundcolor):
        value = StandardTextProcessing.parseStringWithQuotes(self._attributes[key]["value"])
        self._widget.configure(foreground = value)

    def _setWidth(self, elements, key = AttributeNames.width):
        value = self._attributes[key]["value"]
        if value.isdigit():
            self._widget.configure(width = int(value))
        else:
            self._logger.warn("For element " + self._id + " ,setWidth for " + key + " is not a digit: " + value)

    def _setHeight(self, elements, key = AttributeNames.height):
        value = self._attributes[key]["value"]
        if value.isdigit():
            self._widget.configure(height = int(value))
        else:
            self._logger.warn("For element " + self._id + " ,setHeight for " + key + " is not a digit: " + value)

    #----------------------------------------------------------------------------------------------
    #-----Special-Attributes----
    #----------------------------------------------------------------------------------------------

    def _setOnHover(self, elements): 
        on_hover = self._attributes[AttributeNames.onhover]["value"]
        on_hover_background_color = self._attributes[AttributeNames.onhover_background_color]["value"]
        on_hover_foreground_color = StandardTextProcessing.parseStringWithQuotes(on_hover_background_color)

        on_hover_foreground_color = self._attributes[AttributeNames.onhover_foreground_color]["value"]
        on_hover_foreground_color = StandardTextProcessing.parseStringWithQuotes(on_hover_foreground_color)

        if on_hover == "true":
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
                self._base_engine.assume(self._callbacks[key]["policy"])

            self._widget.bind('<Button-1>', clickEvent)

    def _addComponentToElements(self, elements):
        self._widget.pack(expand=True)
        elements[str(self._id)] = self






