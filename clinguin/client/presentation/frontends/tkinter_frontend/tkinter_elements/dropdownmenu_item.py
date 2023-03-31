"""
Contains the DropdownmenuItem class.
"""
import tkinter as tk

from .root_cmp import *


class DropdownmenuItem(RootCmp):
    """
    Is an item of a dropdown, e.g. for the dropdownmenu countries, germany would be a dropdownmenu-item.
    """

    def _init_element(self, elements):
        parent = elements[str(self._parent)]
        if hasattr(parent, "get_menu"):
            menu = parent.get_menu()
            return menu
        else:
            error_string = (
                "Parent of dropdown menu item " + self._id + " is not a dropdown menu."
            )
            self._logger.error(error_string)
            raise Exception(error_string)

    @classmethod
    def _get_attributes(cls, attributes=None):
        if attributes is None:
            attributes = {}

        attributes[AttributeNames.label] = {"value": "", "value_type": StringType}

        return attributes

    @classmethod
    def _get_callbacks(cls, callbacks=None):
        if callbacks is None:
            callbacks = {}

        callbacks[CallbackNames.click] = {"policy": None, "policy_type": SymbolType}

        return callbacks

    def _define_click_event(self, elements, key=CallbackNames.click):
        if self._callbacks[key]:
            self._element["menu"].add_command(
                label=self._attributes[AttributeNames.label]["value"],
                command=CallBackDefinition(
                    self._id,
                    self._parent,
                    self._callbacks[key]["policy"],
                    elements,
                    self._dropdownmenuitem_click,
                ),
            )

    def _dropdownmenuitem_click(self, id, parent_id, click_policy, elements):
        parent = elements[str(parent_id)]
        if hasattr(parent, "get_variable"):
            variable = getattr(parent, "get_variable")()
            variable.set(id)
            if click_policy is not None:
                self._base_engine.post_with_policy(click_policy)
        else:
            self._logger.warning(
                "Could not set variable for dropdownmenu. Item id: %s, dropdown-menu-id: %s",
                str(id),
                str(parent_id),
            )

    def forget_children(self, elements):
        pass
