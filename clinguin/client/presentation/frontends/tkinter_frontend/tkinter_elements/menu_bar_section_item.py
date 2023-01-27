"""
Contains the menu bar section item class.
"""
from .root_cmp import *

class MenuBarSectionItem(RootCmp):
    """
    The menu bar section is a section of a menu bar (e.g. in the menu \|main\|contact\|, where if one clicks on \|contact\| further the options \|location\|team\| appear, a menu-bar-section would be \|contact\|, whereas \|location\| and \|team\| would be menu-bar-section-items.
    """

    def _init_element(self, elements):
        menubar_section = elements[self._parent].get_element()

        return menubar_section

    @classmethod
    def _get_attributes(cls, attributes = None):
        if attributes is None:
            attributes = {}

        attributes[AttributeNames.label] = {"value":"standard_label", "value_type" : StringType}

        return attributes


    @classmethod
    def _get_callbacks(cls, callbacks = None):
        if callbacks is None:
            callbacks = {}

        callbacks[CallbackNames.click] = {"policy":None, "policy_type" : SymbolType}

        return callbacks

    def _define_click_event(self, elements):
        key = CallbackNames.click
        text = self._attributes[AttributeNames.label]["value"]

        if self._callbacks[key] and self._callbacks[key]["policy"]:
            self._element.add_command(
                label=text,
                command=CallBackDefinition(
                    self._id,
                    self._parent,
                    self._callbacks[key]["policy"],
                    elements,
                    self._menubar_item_click))
        else:
            self._element.add_command(
                label=text)


    def _menubar_item_click(self, id, parent, click_policy, elements):
        if click_policy is not None:
            self._base_engine.post_with_policy(click_policy)
 
    def _add_component_to_elements(self, elements):
        elements[str(self._id)] = self

    def forget_children(self, elements):
        pass


