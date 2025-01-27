# pylint: disable=R0801
"""
This module contains the Dropdownmenu class.
"""
import tkinter as tk

from clinguin.utils.attribute_types import (
    BooleanType,
    ColorType,
    StringType,
    SymbolType,
)

from ..tkinter_utils import AttributeNames, CallbackNames, ConfigureSize, LayoutFollower
from .root_cmp import RootCmp


class Dropdownmenu(RootCmp, LayoutFollower, ConfigureSize):
    """
    The dropdownmenu is the master component for a dropdownmenu,
    i.e. dropdownmenu-items must be children of it.
    For available attributes see syntax definition.
    Implementation wise it is similarly implemented as the Label and Button -
    to make it work for layouting, the actual dropdownmenu is hidden and the element
    is actually a tkinter frame (therefore self._element is a frame, whereas self._menu is the dropdownmenu).
    """

    def __init__(self, args, cid, parent, attributes, callbacks, base_engine):
        super().__init__(args, cid, parent, attributes, callbacks, base_engine)

        self._menu = None
        self._variable = None

    def _init_element(self, elements):
        option_menu_frame = tk.Frame(elements[str(self._parent)].get_element())

        self._variable = tk.StringVar()
        items = []
        menu = tk.OptionMenu(option_menu_frame, self._variable, "", *items)

        self._menu = menu

        return option_menu_frame

    def get_variable(self):
        """
        Gets the variable associated with the value.
        """
        return self._variable

    @classmethod
    def _get_attributes(cls, attributes=None):
        if attributes is None:
            attributes = {}

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

        attributes[AttributeNames.selected] = {"value": "", "value_type": StringType}

        return attributes

    @classmethod
    def _get_callbacks(cls, callbacks=None):
        if callbacks is None:
            callbacks = {}

        callbacks[CallbackNames.clear] = {
            "operation": None,
            "operation_type": SymbolType,
        }

        return callbacks

    def _clear_select(self, cid, parent_id, click_operation, elements):
        parent = elements[str(parent_id)]
        if hasattr(parent, "get_variable"):
            variable = getattr(parent, "get_variable")()
            variable.set(cid)
            if click_operation is not None:
                self._base_engine.post_with_operation(click_operation)
        else:
            self._logger.warning(
                "Could not set variable for dropdownmenu. Item id: %s, dropdown-menu-id: %s",
                str(id),
                str(parent_id),
            )

    def _dropdown_clear(self, click_operation):
        variable = self.get_variable()
        variable.set("")
        self._base_engine.post_with_operation(click_operation)

    def _define_clear_event(
        self, elements, key=CallbackNames.clear
    ):  # pylint: disable=W0613
        if self._callbacks[key]["operation"] is None:
            return

        def change(*args):  # pylint: disable=W0613
            if self._variable.get() == "":
                self._logger.info("Will remove previous selections")
                self._dropdown_clear(self._callbacks[key]["operation"])

        self._variable.trace("w", change)

    def _set_background_color(
        self, elements, key=AttributeNames.backgroundcolor
    ):  # pylint: disable=W0613
        value = self._attributes[key]["value"]

        self._menu.config(bg=value, activebackground=value)
        self._menu["menu"].config(bg=value, activebackground=value)

    def _set_foreground_color(
        self, elements, key=AttributeNames.foregroundcolor
    ):  # pylint: disable=W0613
        value = self._attributes[key]["value"]

        self._menu.config(fg=value, activeforeground=value)
        self._menu["menu"].config(fg=value, activeforeground=value)

    def _set_on_hover(self, elements):  # pylint: disable=W0613
        on_hover = self._attributes[AttributeNames.onhover]["value"]

        on_hover_background_color = self._attributes[
            AttributeNames.onhover_background_color
        ]["value"]

        on_hover_foreground_color = self._attributes[
            AttributeNames.onhover_foreground_color
        ]["value"]

        if on_hover == "true":
            self._menu.config(
                activebackground=on_hover_background_color,
                activeforeground=on_hover_foreground_color,
            )
            self._menu["menu"].config(
                activebackground=on_hover_background_color,
                activeforeground=on_hover_foreground_color,
            )

    def _set_selected(self, elements):  # pylint: disable=W0613
        self._variable.set(self._attributes[AttributeNames.selected]["value"])

    def get_menu(self):
        """
        Returns the actual tkinter menu of this element.
        """
        return self._menu

    def _add_component_to_elements(self, elements):
        self._menu.pack(expand=True, fill="both")

        elements[str(self._id)] = self
