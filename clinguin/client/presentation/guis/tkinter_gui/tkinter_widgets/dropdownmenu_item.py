import tkinter as tk

from .root_cmp import *

class DropdownmenuItem(RootCmp):

    def _initWidget(self, elements):
        menu = elements[str(self._parent)].getWidget()
        return menu

    @classmethod
    def getAttributes(cls):
        attributes = {}

        attributes[AttributeNames.label] = {"value":"", "value_type":StringType}

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
                self._base_engine.postWithPolicy(click_policy)
        else:
            self._logger.warn("Could not set variable for dropdownmenu. Item id: " + str(id) + ", dropdown-menu-id: " + str(parent_id))

    def forgetChildren(self, elements):
        pass













