
import tkinter as tk

from .root_cmp import RootCmp

class Dropdownmenu(RootCmp):

    def _defineComponent(self, elements):
        self._variable = tk.StringVar()
        items = []
        menu = tk.OptionMenu(elements[self._parent][0], self._variable, "", *items)

        return menu

    def _defineStandardAttributes(self, standard_attributes):
        standard_attributes["backgroundcolor"] = {"value":"white", "exec":self._setBackgroundColor}
        
    def _setBackgroundColor(self, component, key, standard_attributes):
        component.configure(background = standard_attributes[key]["value"])

    def _defineSpecialAttributes(self, special_attributes):
        special_attributes["selected"] = {"value":""}
        

    def _execSpecialAttributes(self, elements, special_attributes):
        if special_attributes["selected"]['value'] != "":
            self._variable.set(special_attributes["selected"]['value'])

    def _addComponentToElements(self, elements):
        self._component.pack(expand=True)
        elements[str(self._id)] = (self._component, {"variable": self._variable})





