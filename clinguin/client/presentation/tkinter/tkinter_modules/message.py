from tkinter import font
import tkinter as tk
import tkinter.messagebox

from .root_cmp import RootCmp
from .standard_text_processing import StandardTextProcessing

from .attribute_names import AttributeNames
from .callback_names import CallbackNames


class Message(RootCmp):


    def _initWidget(self, elements):
        message = tk.Message(elements[str(self._parent)].getWidget())
        return message

    @classmethod
    def getAttributes(cls):
        attributes = {}
        attributes[AttributeNames.type] = {"value":""}
        attributes[AttributeNames.title] = {"value":""}
        attributes[AttributeNames.message] = {"value":""}

        return attributes

    def _setValues(self, elements):

        title = self._attributes[AttributeNames.title]["value"]
        title = StandardTextProcessing.parseStringWithQuotes(title)

        message = self._attributes[AttributeNames.message]["value"]
        message = StandardTextProcessing.parseStringWithQuotes(message)

        tk.messagebox.showinfo(title=title, message=message)


