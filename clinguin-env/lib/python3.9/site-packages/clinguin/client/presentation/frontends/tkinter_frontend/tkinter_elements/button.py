# pylint: disable=R0801
"""
This module contains the button class.
"""
import tkinter as tk

from clinguin.utils.attribute_types import (
    BooleanType,
    ColorType,
    StringType,
    SymbolType,
)

from ..tkinter_utils import (
    AttributeNames,
    CallbackNames,
    ConfigureFont,
    ConfigureSize,
    ConfigureTextElementSize,
    LayoutFollower,
)
from .root_cmp import RootCmp


class Button(
    RootCmp, LayoutFollower, ConfigureSize, ConfigureFont, ConfigureTextElementSize
):
    """
    A button is a element, which is generally regarded as an active element,
    so actions are executed. For available attributes see syntax definition.
    Implementation wise it is similarly implemented as the Label and Dropdownmenu -
    to make it work for layouting, the actual button is hidden the the element is actually
    a tkinter frame (therefore self._element is a frame, whereas self._button is the button).
    """

    def __init__(self, args, cid, parent, attributes, callbacks, base_engine):
        super().__init__(args, cid, parent, attributes, callbacks, base_engine)

        self._button = None

    def _init_element(self, elements):
        button_frame = tk.Frame(elements[str(self._parent)].get_element())

        self._button = tk.Button(button_frame)
        self._configure_font_element = self._button
        self._configure_text_element_size = self._button

        return button_frame

    @classmethod
    def _get_attributes(cls, attributes=None):
        if attributes is None:
            attributes = {}

        # Label/Text
        attributes[AttributeNames.label] = {"value": "", "value_type": StringType}
        # Color
        attributes[AttributeNames.backgroundcolor] = {
            "value": "white",
            "value_type": ColorType,
        }
        attributes[AttributeNames.foregroundcolor] = {
            "value": "black",
            "value_type": ColorType,
        }
        # Interactive-Attributes
        attributes[AttributeNames.onhover] = {"value": False, "value_type": BooleanType}
        attributes[AttributeNames.onhover_background_color] = {
            "value": "white",
            "value_type": ColorType,
        }
        attributes[AttributeNames.onhover_foreground_color] = {
            "value": "black",
            "value_type": ColorType,
        }

        return attributes

    @classmethod
    def _get_callbacks(cls, callbacks=None):
        if callbacks is None:
            callbacks = {}

        callbacks[CallbackNames.click] = {
            "operation": None,
            "operation_type": SymbolType,
        }

        return callbacks

    # ----------------------------------------------------------------------------------------------
    # -----Attributes----
    # ----------------------------------------------------------------------------------------------

    def _set_label_text(self, elements):
        self._logger.debug(str(elements))
        text = self._attributes[AttributeNames.label]["value"]
        self._button.configure(text=text)

    def _set_background_color(self, elements, key=AttributeNames.backgroundcolor):
        self._logger.debug(str(elements))
        value = self._attributes[key]["value"]
        self._button.configure(background=value)

    def _set_foreground_color(self, elements, key=AttributeNames.foregroundcolor):
        self._logger.debug(str(elements))
        value = self._attributes[key]["value"]
        self._button.configure(foreground=value)

    def _set_on_hover(self, elements):
        on_hover = self._attributes[AttributeNames.onhover]["value"]
        on_hover_background_color = self._attributes[
            AttributeNames.onhover_background_color
        ]["value"]

        on_hover_foreground_color = self._attributes[
            AttributeNames.onhover_foreground_color
        ]["value"]

        if on_hover:

            def enter(event):
                self._logger.debug(str(event))
                if on_hover_background_color != "":
                    self._set_background_color(
                        elements, key=AttributeNames.onhover_background_color
                    )
                if on_hover_foreground_color != "":
                    self._set_foreground_color(
                        elements, key=AttributeNames.onhover_foreground_color
                    )

            def leave(event):
                self._logger.debug(str(event))
                self._set_background_color(elements)
                self._set_foreground_color(elements)

            self._button.bind("<Enter>", enter)
            self._button.bind("<Leave>", leave)

    # ----------------------------------------------------------------------------------------------
    # -----Actions----
    # ----------------------------------------------------------------------------------------------

    def _define_click_event(self, elements):
        self._logger.debug(str(elements))
        key = CallbackNames.click
        if self._callbacks[key] and self._callbacks[key]["operation"]:

            def click_event(event):
                self._logger.debug(str(event))
                self._base_engine.post_with_operation(self._callbacks[key]["operation"])

            self._button.bind("<Button-1>", click_event)

    def _add_component_to_elements(self, elements):
        self._button.pack(expand=True, fill="both")

        elements[str(self._id)] = self
