"""
Contains the menu bar section item class.
"""
from .root_cmp import *

class MenuBarSectionItem(RootCmp):
    """
    The menu bar section is a section of a menu bar (e.g. in the menu \|main\|contact\|, where if one clicks on \|contact\| further the options \|location\|team\| appear, a menu-bar-section would be \|contact\|, whereas \|location\| and \|team\| would be menu-bar-section-items.
    """

    def _initWidget(self, elements):
        menubar_section = elements[self._parent].getWidget()

        return menubar_section

    @classmethod
    def _getAttributes(cls, attributes = None):
        if attributes is None:
            attributes = {}

        attributes[AttributeNames.label] = {"value":"standard_label", "value_type" : StringType}

        return attributes


    @classmethod
    def _getCallbacks(cls, callbacks = None):
        if callbacks is None:
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
        if click_policy is not None:
            self._base_engine.postWithPolicy(click_policy)
 
    def _addComponentToElements(self, elements):
        elements[str(self._id)] = self

    def forgetChildren(self, elements):
        pass


