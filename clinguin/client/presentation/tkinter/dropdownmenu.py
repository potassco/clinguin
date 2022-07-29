
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
        standard_attributes["foregroundcolor"] = {"value":"black", "exec":self._setForegroundColor}

    def _defineSpecialAttributes(self, special_attributes):
        # Interactive-Attributes
        special_attributes["onhover"] = {"value":"false"}
        special_attributes["onhoverbackgroundcolor"] = {"value":""}
        special_attributes["onhoverforegroundcolor"] = {"value":""}
        
        special_attributes["selected"] = {"value":""}
        
    def _setBackgroundColor(self, component, key, standard_attributes):
        value = standard_attributes[key]["value"]
        
        component.config(bg= value, activebackground=value)
        component["menu"].config(bg=value, activebackground=value)

    def _setForegroundColor(self, component, key, standard_attributes):
        value = standard_attributes[key]["value"]

        component.config(fg=value, activeforeground=value)
        component["menu"].config(fg=value, activeforeground=value)

    def _execSpecialAttributes(self, elements, standard_attributes, special_attributes):
        self._setSelected(elements, standard_attributes, special_attributes)
        self._setOnHover(elements, standard_attributes, special_attributes)
 
    def _setOnHover(self, elements, standard_attributes, special_attributes): 
        on_hover = special_attributes["onhover"]["value"]
        on_hover_background_color = special_attributes["onhoverbackgroundcolor"]["value"]
        on_hover_foreground_color = special_attributes["onhoverforegroundcolor"]["value"]

        if on_hover == "true":
            self._component.config(activebackground=on_hover_background_color, activeforeground=on_hover_foreground_color)
            self._component["menu"].config(activebackground=on_hover_background_color, activeforeground=on_hover_foreground_color)

            """
            def enter(event):
                if on_hover_background_color != "":
                    self._setBackgroundColor(self._component, "onhoverbackgroundcolor", special_attributes)
                if on_hover_foreground_color != "":
                    self._setForegroundColor(self._component, "onhoverforegroundcolor", special_attributes)

            def leave(event):
                self._setBackgroundColor(self._component, "backgroundcolor", standard_attributes)
                self._setForegroundColor(self._component, "foregroundcolor", standard_attributes)
    
            self._component.bind('<Enter>', enter)
            self._component.bind('<Leave>', leave)
            """
 

    def _setSelected(self, elements, standard_attributes, special_attributes):
        if special_attributes["selected"]['value'] != "":
            self._variable.set(special_attributes["selected"]['value'])

    def _addComponentToElements(self, elements):
        self._component.pack(expand=True)
        elements[str(self._id)] = (self._component, {"variable": self._variable})





