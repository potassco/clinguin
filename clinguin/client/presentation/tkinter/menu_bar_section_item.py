import tkinter as tk

from clinguin.client.presentation.tkinter.root_cmp import RootCmp
from clinguin.client.presentation.tkinter.call_back_definition import CallBackDefinition
from clinguin.client.presentation.tkinter.standard_text_processing import StandardTextProcessing

class MenuBarSectionItem(RootCmp):

    def _defineComponent(self, elements):
        menubar_section = elements[self._parent].getWidget()

        return menubar_section

    def _defineStandardAttributes(self, standard_attributes):
        standard_attributes["label"] = {"value":"standard_label", "exec":self._doNothing}

    def _defineActions(self, actions):
        actions["click"] = {"policy":None, "exec":self._defineClickEvent}

    def _doNothing(self, component, key, standard_attributes):
        pass
       
    def _defineClickEvent(self, component, key, actions, standard_attributes, special_attributes, elements):
        value = standard_attributes["label"]["value"]
        text = StandardTextProcessing.parseStringWithQuotes(value)

        if actions[key] and actions[key]["policy"]:
            component.add_command(
                label=text,
                command=CallBackDefinition(
                    self._id,
                    self._parent,
                    actions[key]["policy"],
                    elements,
                    self._menubarItemClick))
        else:
            component.add_command(
                label=text)


    def _menubarItemClick(self, id, parent, click_policy, elements):
        if (click_policy is not None):
            self._base_engine.assume(click_policy)
 
    def _addComponentToElements(self, elements):
        elements[str(self._id)] = self

    def forgetChildren(self, elements):
        pass


