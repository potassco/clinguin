"""
This module contains the Label class.
"""
import tkinter as tk

from .root_cmp import *

class Label(RootCmp, LayoutFollower, ConfigureSize, ConfigureFont):
    """
    The label can be used for positiion text. For available attributes see syntax definition. Implementation wise it is similarly implemented as the Dropdowmenu and Button - to make it work for layouting, the actual label is hidden and the widget is actually a tkinter frame (therefore self._widget is a frame, whereas self._label is the label).
    """
    def __init__(self, args, id, parent, attributes, callbacks, base_engine):
        super().__init__(args, id, parent, attributes, callbacks, base_engine)
        self._configure_font_widget = None
        self._label = None

    def _initWidget(self, elements):
        label_frame = tk.Frame(elements[str(self._parent)].getWidget())

        self._label = tk.Label(label_frame)
        self._configure_font_widget = self._label

        return label_frame

    @classmethod
    def _getAttributes(cls, attributes = None):
        if attributes is None:
            attributes = {}

        attributes[AttributeNames.label] = {"value":"", "value_type" : StringType}
        attributes[AttributeNames.backgroundcolor] = {"value":"white", "value_type" : ColorType}
        attributes[AttributeNames.foregroundcolor] = {"value":"black", "value_type" : ColorType}
        # Interactive-Attributes
        attributes[AttributeNames.onhover] = {"value":False, "value_type" : BooleanType}
        attributes[AttributeNames.onhover_background_color] = {"value":"white", "value_type" : ColorType}
        attributes[AttributeNames.onhover_foreground_color] = {"value":"black", "value_type" : ColorType}
        return attributes

    @classmethod
    def _getCallbacks(cls, callbacks = None):
        if callbacks is None:
            callbacks = {}

        callbacks[CallbackNames.click] = {"policy":None, "policy_type": SymbolType}

        return callbacks

    #----------------------------------------------------------------------------------------------
    #-----Standard-Attributes----
    #----------------------------------------------------------------------------------------------

    def _setLabelText(self, elements, key = AttributeNames.label):
        text = self._attributes[key]["value"]
        self._label.configure(text = text)

    def _setBackgroundColor(self, elements, key = AttributeNames.backgroundcolor):
        value = self._attributes[key]["value"]
        self._label.configure(background = value)

    def _setForegroundColor(self, elements, key = AttributeNames.foregroundcolor):
        value = self._attributes[key]["value"]
        self._label.configure(foreground = value)

    #----------------------------------------------------------------------------------------------
    #-----Special-Attributes----
    #----------------------------------------------------------------------------------------------

    def _setOnHover(self, elements): 
        on_hover = self._attributes[AttributeNames.onhover]["value"]
        on_hover_background_color = self._attributes[AttributeNames.onhover_background_color]["value"]

        on_hover_foreground_color = self._attributes[AttributeNames.onhover_foreground_color]["value"]

        if on_hover:
            def enter(event):
                if on_hover_background_color != "":
                    self._setBackgroundColor(elements, key = AttributeNames.onhover_background_color)
                if on_hover_foreground_color != "":
                    self._setForegroundColor(elements, key = AttributeNames.onhover_foreground_color)

            def leave(event):
                self._setBackgroundColor(elements, key = AttributeNames.backgroundcolor)
                self._setForegroundColor(elements, key= AttributeNames.foregroundcolor)
    
            self._label.bind('<Enter>', enter)
            self._label.bind('<Leave>', leave)

 
    #----------------------------------------------------------------------------------------------
    #-----Actions----
    #----------------------------------------------------------------------------------------------
       
    def _defineClickEvent(self, elements):
        key = CallbackNames.click
        if self._callbacks[key] and self._callbacks[key]["policy"]:
            def clickEvent(event):
                self._base_engine.postWithPolicy(self._callbacks[key]["policy"])

            self._label.bind('<Button-1>', clickEvent)

    def _addComponentToElements(self, elements):
        self._label.pack(expand=True, fill='both')

        elements[str(self._id)] = self






