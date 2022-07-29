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
        standard_attributes["childorg"] = {"value":"flex", "exec":self._setChildOrg}
        standard_attributes["borderwidth"] = {"value":str(0), "exec":self._setBorderWidth}
        standard_attributes["bordercolor"] = {"value":"black", "exec":self._setBorderBackgroundColor}

    def _setBackgroundColor(self, component, key, standard_attributes):
        component.configure(background = standard_attributes[key]["value"])

    def _setWidth(self, component, key, standard_attributes):
        component.configure(width = int(standard_attributes[key]["value"]))

    def _setHeight(self, component, key, standard_attributes):
        component.configure(height = int(standard_attributes[key]["value"]))

    def _setChildOrg(self, component, key, standard_attributes):
        self._child_org = standard_attributes[key]["value"]

    def _setBorderWidth(self, component, key, standard_attributes):
        value = standard_attributes[key]["value"]
        if value.isdigit():
            if int(value) > 0:
                # Not using borderwidth as one cannot set the color of the default border
                component.configure(highlightthickness = int(value))
        else:
            self._logger.warn("setBorderwidth for " + key + " is not a digit: " + value)

    def _setBorderBackgroundColor(self, component, key, standard_attributes):
        # Not using borderwidth as one cannot set the color of the default border
        value = standard_attributes[key]["value"]
        component.configure(highlightbackground = value, highlightcolor = value)

    def _defineSpecialAttributes(self, special_attributes):
        special_attributes["gridx"] = {"value":str(0)}
        special_attributes["gridy"] = {"value":str(0)}

        special_attributes["onhover"] = {"value":"false"}
        special_attributes["onhoverbackgroundcolor"] = {"value":""}
        special_attributes["onhoverbordercolor"] = {"value":""}

    def _execSpecialAttributes(self, elements, standard_attributes, special_attributes):
        self._setLayout(elements, standard_attributes, special_attributes)

        self._setOnHover(elements, standard_attributes, special_attributes)
   
    def _setLayout(self, elements, standard_attributes, special_attributes):
        parent_org = elements[self._parent][1]["childorg"]

        if parent_org == "flex":
            self._component.pack(expand=True)
        elif parent_org == "grid" and int(special_attributes["gridx"]['value']) >= 0 and int(special_attributes["gridy"]['value']) >= 0:
            self._component.grid(
                column=int(special_attributes["gridx"]['value']), 
                row=int(special_attributes["gridy"]['value']))
        elif parent_org == "static":
            print("STATIC")


    def _setOnHover(self, elements, standard_attributes, special_attributes): 
        on_hover = special_attributes["onhover"]["value"]
        on_hover_color = special_attributes["onhoverbackgroundcolor"]["value"]
        on_hover_border_color = special_attributes["onhoverbordercolor"]["value"]

        if on_hover == "true":
            def enter(event):
                if on_hover_color != "":
                    self._component.configure(background = on_hover_color)
                if on_hover_border_color != "":
                    self._component.configure(highlightbackground = on_hover_border_color, highlightcolor = on_hover_color)

            def leave(event):
                self._setBackgroundColor(self._component, "backgroundcolor", standard_attributes)
                self._setBorderBackgroundColor(self._component, "bordercolor", standard_attributes)
    
            self._component.bind('<Enter>', enter)
            self._component.bind('<Leave>', leave)
        

    def _addComponentToElements(self, elements):
        self._component.pack_propagate(0)
        elements[str(self._id)] = (self._component, {"childorg":self._child_org})






