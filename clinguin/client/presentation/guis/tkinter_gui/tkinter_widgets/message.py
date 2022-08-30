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

        attributes[AttributeNames.type] = {"value":"", "value_type" : StringType}
        attributes[AttributeNames.title] = {"value":"", "value_type" : StringType}
        attributes[AttributeNames.message] = {"value":"", "value_type" : StringType}

        return attributes

    def _setValues(self, elements):

        title = self._attributes[AttributeNames.title]["value"]

        message = self._attributes[AttributeNames.message]["value"]

        tk.messagebox.showinfo(title=title, message=message)


