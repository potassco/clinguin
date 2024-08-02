# pylint: disable=R0801
"""
Contains the DropdownmenuItem class.
"""

from clinguin.utils.attribute_types import StringType, SymbolType

from ..tkinter_utils import AttributeNames, CallBackDefinition, CallbackNames
from .root_cmp import RootCmp


class DropdownmenuItem(RootCmp):
    """
    Is an item of a dropdown, e.g. for the dropdownmenu countries, germany would be a dropdownmenu-item.
    """

    def _init_element(self, elements):
        parent = elements[str(self._parent)]
        if hasattr(parent, "get_menu"):
            menu = parent.get_menu()
        else:
            error_string = (
                "Parent of dropdown menu item " + self._id + " is not a dropdown menu."
            )
            self._logger.error(error_string)
            raise Exception(error_string)

        return menu

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

        callbacks[CallbackNames.click] = {
            "operation": None,
            "operation_type": SymbolType,
        }

        return callbacks

    def _define_click_event(self, elements, key=CallbackNames.click):
        if self._callbacks[key]:
            self._element["menu"].add_command(
                label=self._attributes[AttributeNames.label]["value"],
                command=CallBackDefinition(
                    self._id,
                    self._parent,
                    self._callbacks[key]["operation"],
                    elements,
                    self._dropdownmenuitem_click,
                ),
            )

    def _dropdownmenuitem_click(self, cid, parent_id, click_operation, elements):
        parent = elements[str(parent_id)]
        if hasattr(parent, "get_variable"):
            variable = getattr(parent, "get_variable")()
            variable.set(cid)
            if click_operation is not None:
                self._base_engine.post_with_operation(click_operation)
        else:
            self._logger.warning(
                "Could not set variable for dropdownmenu. Item id: %s, dropdown-menu-id: %s",
                str(cid),
                str(parent_id),
            )

    def forget_children(self, elements):
        pass  # pylint: disable=W0107
