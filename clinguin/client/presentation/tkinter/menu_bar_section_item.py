import tkinter as tk

from clinguin.client.presentation.tkinter.root_cmp import RootCmp
from clinguin.client.presentation.tkinter.call_back_definition import CallBackDefinition
from clinguin.client.presentation.tkinter.standard_text_processing import StandardTextProcessing

from clinguin.client.presentation.tkinter.attribute_names import AttributeNames
from clinguin.client.presentation.tkinter.callback_names import CallbackNames


class MenuBarSectionItem(RootCmp):

    def _initWidget(self, elements):
        menubar_section = elements[self._parent].getWidget()

        return menubar_section

    @classmethod
    def getAttributes(cls):
        attributes = {}

        attributes[AttributeNames.label] = {"value":"standard_label"}

        return attributes


    @classmethod
    def getCallbacks(cls):
        callbacks = {}

        callbacks[CallbackNames.click] = {"policy":None}

        return callbacks

    def _defineClickEvent(self, elements):
        key = CallbackNames.click
        value = self._attributes[AttributeNames.label]["value"]
        text = StandardTextProcessing.parseStringWithQuotes(value)

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
            self._base_engine.assume(click_policy)
 
    def _addComponentToElements(self, elements):
        elements[str(self._id)] = self

    def forgetChildren(self, elements):
        pass


