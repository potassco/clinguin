import tkinter as tk

from .root_cmp import RootCmp

class Container(RootCmp):

    def _defineComponent(self, elements):
        container = tk.Frame(elements[str(self._parent)][0])
        return container

    def _defineStandardAttributes(self, standard_attributes):
        standard_attributes["backgroundcolor"] = {"value":"white", "exec":self._setBackgroundColor}
        standard_attributes["width"] = {"value":str(50), "exec":self._setWidth}
        standard_attributes["height"] = {"value":str(50), "exec":self._setHeight}
        standard_attributes["childorg"] = {"value":"grid", "exec":self._setChildOrg}

    def _setBackgroundColor(self, component, key, standard_attributes):
        component.configure(background = standard_attributes[key]["value"])

    def _setWidth(self, component, key, standard_attributes):
        component.configure(width = int(standard_attributes[key]["value"]))

    def _setHeight(self, component, key, standard_attributes):
        component.configure(height = int(standard_attributes[key]["value"]))

    def _setChildOrg(self, component, key, standard_attributes):
        self._child_org = standard_attributes[key]["value"]

    def _defineSpecialAttributes(self, special_attributes):
        special_attributes["gridx"] = {"value":str(0)}
        special_attributes["gridy"] = {"value":str(0)}

    def _execSpecialAttributes(self, elements, special_attributes):
        if elements[self._parent][1]["childorg"] == "grid" and int(special_attributes["gridx"]['value']) >= 0 and int(special_attributes["gridy"]['value']) >= 0:
            self._component.grid(
                column=int(special_attributes["gridx"]['value']), 
                row=int(special_attributes["gridy"]['value']))


    def _addComponentToElements(self, elements):
        self._component.pack_propagate(0)
        elements[str(self._id)] = (self._component, {"childorg":self._child_org})






