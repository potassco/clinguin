from tkinter import font
import tkinter as tk
import tkinter.messagebox

from .root_cmp import *

class Message(RootCmp):


    def _initWidget(self, elements):
        message = tk.Message(elements[str(self._parent)].getWidget())
        return message

    @classmethod
    def getAttributes(cls):
        attributes = {}
        attributes[AttributeNames.type] = {"value":"", "value_type" : StringType}
        attributes[AttributeNames.title] = {"value":"", "value_type" : StringType}
        attributes[AttributeNames.message] = {"value":"", "value_type" : StringType}

        return attributes

    def _setValues(self, elements):

        title = self._attributes[AttributeNames.title]["value"]

        message = self._attributes[AttributeNames.message]["value"]

        tk.messagebox.showinfo(title=title, message=message)


