import tkinter as tk

from .root_cmp import *

class MenuBarSectionItem(RootCmp):

    def _initWidget(self, elements):
        menubar_section = elements[self._parent].getWidget()

        return menubar_section

    @classmethod
    def getAttributes(cls):
        attributes = {}

        attributes[AttributeNames.label] = {"value":"standard_label", "value_type" : StringType}

        return attributes


    @classmethod
    def getCallbacks(cls):
        callbacks = {}

        callbacks[CallbackNames.click] = {"policy":None, "policy_type" : SymbolType}

        return callbacks

    def _defineClickEvent(self, elements):
        key = CallbackNames.click
        text = self._attributes[AttributeNames.label]["value"]

        if self._callbacks[key] and self._callbacks[key]["policy"]:
            self._widget.add_command(
                label=text,
                command=CallBackDefinition(
                    self._id,
                    self._parent,
                    self._callbacks[key]["policy"],
                    elements,
                    self._menubarItemClick))
        else:
            self._widget.add_command(
                label=text)


    def _menubarItemClick(self, id, parent, click_policy, elements):
        if (click_policy is not None):
            self._base_engine.postWithPolicy(click_policy)
 
    def _addComponentToElements(self, elements):
        elements[str(self._id)] = self

    def forgetChildren(self, elements):
        pass


