# pylint: disable=R0801
"""
Contains the menu bar section item class.
"""

from clinguin.utils.attribute_types import StringType, SymbolType

from ..tkinter_utils import AttributeNames, CallBackDefinition, CallbackNames
from .root_cmp import RootCmp

key_map = {
    "Ctrl": "Control",
    "Opt": "Option",
    "Cmd": "Command",
    "Control": "Control",
    "Option": "Option",
    "Command": "Command",
    "Shift": "Shift",
}


def accelerator_to_bind(a):
    """
    Getting key bindings as string.
    """
    args = a.split("+")
    formatted = []
    for e in args:
        if e in key_map:
            formatted.append(key_map[e])
        else:
            formatted.append(e.lower())
    return "<" + "-".join(formatted) + ">"


class MenuBarSectionItem(RootCmp):
    """
    The menu bar section is a section of a menu bar (e.g. in the menu |main|contact|,
    where if one clicks on |contact| further the options |location|team| appear,
    a menu-bar-section would be |contact|, whereas |location| and |team| would be menu-bar-section-items.
    """

    def _init_element(self, elements):
        menubar_section = elements[self._parent].get_element()

        return menubar_section

    @classmethod
    def _get_attributes(cls, attributes=None):
        if attributes is None:
            attributes = {}

        attributes[AttributeNames.label] = {
            "value": "standard_label",
            "value_type": StringType,
        }
        attributes[AttributeNames.accelerator] = {
            "value": None,
            "value_type": StringType,
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

    def _define_click_event(self, elements):
        key = CallbackNames.click
        text = self._attributes[AttributeNames.label]["value"]
        accelerator = self._attributes[AttributeNames.accelerator]["value"]
        if self._callbacks[key] and self._callbacks[key]["operation"]:
            cb = CallBackDefinition(
                self._id,
                self._parent,
                self._callbacks[key]["operation"],
                elements,
                self._menubar_item_click,
            )
            self._element.add_command(label=text, command=cb, accelerator=accelerator)
            menu = elements[self._parent]
            window = elements[menu.get_parent()]
            root = elements[window.get_parent()]
            if accelerator:
                root.get_element().bind(accelerator_to_bind(accelerator), cb)
        else:
            self._element.add_command(label=text)

    def _menubar_item_click(self, cid, parent, click_operation, elements):
        self._logger.debug(str(cid))
        self._logger.debug(str(parent))
        self._logger.debug(str(elements))

        if click_operation is not None:
            self._base_engine.post_with_operation(click_operation)

    def _add_component_to_elements(self, elements):
        elements[str(self._id)] = self

    def forget_children(self, elements):
        self._logger.debug(str(elements))
        # pylint: disable=W0107
        # pylint: enable=W0107
