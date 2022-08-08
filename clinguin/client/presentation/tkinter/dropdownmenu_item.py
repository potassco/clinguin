import tkinter as tk

from clinguin.client.presentation.tkinter.root_cmp import RootCmp
from clinguin.client.presentation.tkinter.call_back_definition import CallBackDefinition

from clinguin.client.presentation.tkinter.attribute_names import AttributeNames
from clinguin.client.presentation.tkinter.callback_names import CallbackNames

class DropdownmenuItem(RootCmp):

    def _initWidget(self, elements):
        menu = elements[str(self._parent)].getWidget()
        return menu

    @classmethod
    def getAttributes(cls):
        attributes = {}

        attributes[AttributeNames.label] = {"value":""}

        return attributes

    @classmethod
    def getCallbacks(cls):
        callbacks =  {}

        callbacks[CallbackNames.click] = {"policy":None}

        return callbacks

    def _defineClickEvent(self, elements, key = CallbackNames.click):
        if self._callbacks[key]:
            self._widget['menu'].add_command(
                label=self._attributes[AttributeNames.label]["value"],
                command=CallBackDefinition(
                    self._id,
                    self._parent,
                    self._callbacks[key]['policy'],
                    elements,
                    self._dropdownmenuitemClick))

    def _dropdownmenuitemClick(self, id, parent_id, click_policy, elements):
        parent = elements[str(parent_id)]
        if hasattr(parent, "getVariable"):
            variable = getattr(parent, "getVariable")()
            variable.set(id)
            if (click_policy is not None):
                self._base_engine.assume(click_policy)
        else:
            self._logger.warn("Could not set variable for dropdownmenu. Item id: " + str(id) + ", dropdown-menu-id: " + str(parent_id))

    def forgetChildren(self, elements):
        pass













