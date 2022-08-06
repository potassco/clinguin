from tkinter import font
import tkinter as tk
import tkinter.messagebox

from .root_cmp import RootCmp
from .standard_text_processing import StandardTextProcessing

from .attribute_names import AttributeNames
from .callback_names import CallbackNames


class Message(RootCmp):


    def _initWidget(self, elements):
        message = tk.Message()
        return message

    @classmethod
    def getAttributes(cls):
        attributes = {}
        attributes[AttributeNames.type] = {"value":""}
        attributes[AttributeNames.title] = {"value":""}
        attributes[AttributeNames.message] = {"value":""}

        return attributes

    def _setValues(self, elements):
        tk.messagebox.showinfo(title=self._attributes["title"], message=self._attributes["message"])

    def addComponent(self, elements):
        self._attributes = self.__class__.getAttributes()
        self._fillAttributes()
        self._execAttributes(elements)


