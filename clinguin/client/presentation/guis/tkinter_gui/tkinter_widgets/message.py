"""
Contains the Message class.
"""
import tkinter as tk
# This import is used implicitly
import tkinter.messagebox

from .root_cmp import *

class Message(RootCmp):
    """
    A message is a pop up, which has a type a title and a message.
    """


    def _initWidget(self, elements):
        message = tk.Message(elements[str(self._parent)].getWidget())
        return message

    @classmethod
    def _getAttributes(cls, attributes = None):
        if attributes is None:
            attributes = {}

        attributes[AttributeNames.type] = {"value":PopupTypesType.INFO, "value_type" : PopupTypesType}
        attributes[AttributeNames.title] = {"value":"", "value_type" : StringType}
        attributes[AttributeNames.message] = {"value":"", "value_type" : StringType}

        return attributes

    def _setValues(self, elements):

        type = self._attributes[AttributeNames.type]["value"]
        title = self._attributes[AttributeNames.title]["value"]
        message = self._attributes[AttributeNames.message]["value"]

        print(type)
        if PopupTypesType.INFO == type:
            tk.messagebox.showinfo(title=title, message=message)
        elif PopupTypesType.WARNING == type:
            tk.messagebox.showwarning(title=title, message=message)
        elif PopupTypesType.ERROR == type:
            tk.messagebox.showerror(title=title, message=message)
        else:
            self._logger.warning("Cannot display popup-type %s", type)

