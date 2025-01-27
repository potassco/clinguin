# pylint: disable=R0801
"""
Module contains the Container class.
"""
import tkinter as tk

from clinguin.utils.attribute_types import BooleanType, ColorType, SymbolType

from ..tkinter_utils import (
    AttributeNames,
    CallbackNames,
    ConfigureBorder,
    ConfigureSize,
    LayoutController,
    LayoutFollower,
)
from .root_cmp import RootCmp


class Container(
    RootCmp, LayoutFollower, LayoutController, ConfigureSize, ConfigureBorder
):
    """
    The container is a generic element which can be used for layouting,
    hovering effects or even callbacks. Generally it is recommended to use
    it as a ''container'' for multiple other elements, e.g. labels, buttons, etc.
    """

    def _init_element(self, elements):
        container = tk.Frame(elements[str(self._parent)].get_element())
        return container

    @classmethod
    def _get_attributes(cls, attributes=None):
        if attributes is None:
            attributes = {}

        attributes[AttributeNames.backgroundcolor] = {
            "value": "white",
            "value_type": ColorType,
            "description": "CUSTOM-BACKGROUND-COLOR-DESCRIPTION <- Now normal:"
            + AttributeNames.descriptions[AttributeNames.backgroundcolor],
        }
        # Interactive-Attributes
        attributes[AttributeNames.onhover] = {"value": False, "value_type": BooleanType}
        attributes[AttributeNames.onhover_background_color] = {
            "value": "",
            "value_type": ColorType,
        }
        attributes[AttributeNames.onhover_border_color] = {
            "value": "",
            "value_type": ColorType,
        }

        return attributes

    @classmethod
    def _get_callbacks(cls, callbacks=None):
        if callbacks is None:
            callbacks = {}

        callbacks["click"] = {"operation": None, "operation_type": SymbolType}

        return callbacks

    # ----------------------------------------------------------------------------------------------
    # -----Attributes----
    # ----------------------------------------------------------------------------------------------

    def _set_background_color(self, elements, key=AttributeNames.backgroundcolor):
        self._logger.debug(str(elements))
        value = self._attributes[key]["value"]
        self._element.configure(background=value)

    def _set_on_hover(self, elements):
        on_hover = self._attributes[AttributeNames.onhover]["value"]
        on_hover_color = self._attributes[AttributeNames.onhover_background_color][
            "value"
        ]
        on_hover_border_color = self._attributes[AttributeNames.onhover_border_color][
            "value"
        ]

        if on_hover:

            def enter(event):
                self._logger.debug(str(event))
                if on_hover_color != "":
                    self._set_background_color(
                        elements, key=AttributeNames.onhover_background_color
                    )
                if on_hover_border_color != "":
                    self._set_border_background_color(
                        elements, key=AttributeNames.onhover_border_color
                    )

            def leave(event):
                self._logger.debug(str(event))
                self._set_background_color(elements, key=AttributeNames.backgroundcolor)
                self._set_border_background_color(
                    elements, key=AttributeNames.border_color
                )

            self._element.bind("<Enter>", enter)
            self._element.bind("<Leave>", leave)

    # ----------------------------------------------------------------------------------------------
    # -----Actions----
    # ----------------------------------------------------------------------------------------------

    def _define_click_event(self, elements, key=CallbackNames.click):
        self._logger.debug(str(elements))
        if self._callbacks[key] and self._callbacks[key]["operation"]:

            def dropdown_menu_item_click(event):
                self._logger.debug(str(event))
                self._base_engine.assume(self._callbacks[key]["operation"])

            self._element.bind("<Button-1>", dropdown_menu_item_click)
