"""
Contains the Message class.
"""

import tkinter as tk
from tkinter import messagebox

# This import is used implicitly
from clinguin.utils.attribute_types import PopupTypesType, StringType

from ..tkinter_utils import AttributeNames
from .root_cmp import RootCmp


class Message(RootCmp):
    """
    A message is a pop up, which has a type a title and a message.
    """

    def _init_element(self, elements):
        message = tk.Message(elements[str(self._parent)].get_element())
        return message

    @classmethod
    def _get_attributes(cls, attributes=None):
        if attributes is None:
            attributes = {}

        attributes[AttributeNames.type] = {
            "value": PopupTypesType.INFO,
            "value_type": PopupTypesType,
        }
        attributes[AttributeNames.title] = {"value": "", "value_type": StringType}
        attributes[AttributeNames.message] = {"value": "", "value_type": StringType}

        return attributes

    def _set_values(self, elements):
        self._logger.debug(str(elements))
        attr_type = self._attributes[AttributeNames.type]["value"]
        title = self._attributes[AttributeNames.title]["value"]
        message = self._attributes[AttributeNames.message]["value"]
        if PopupTypesType.INFO == attr_type:
            messagebox.showinfo(title=title, message=message)
        elif PopupTypesType.WARNING == attr_type:
            messagebox.showwarning(title=title, message=message)
        elif attr_type in ["danger", PopupTypesType.ERROR]:
            messagebox.showerror(title=title, message=message)
        else:
            self._logger.warning("Cannot display popup-type %s", attr_type)
