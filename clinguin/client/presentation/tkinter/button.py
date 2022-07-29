from tkinter import font
import tkinter as tk

from .root_cmp import RootCmp

class Button(RootCmp):

    def _defineComponent(self, elements):
        button = tk.Button(elements[str(self._parent)][0])
        return button

    def _defineStandardAttributes(self, standard_attributes):
        standard_attributes["label"] = {"value":"", "exec":self._setLabelText}
        standard_attributes["backgroundcolor"] = {"value":"white", "exec":self._setBackgroundColor}
        standard_attributes["foregroundcolor"] = {"value":"black", "exec":self._setForegroundColor}
        standard_attributes["width"] = {"value":str(50), "exec":self._setWidth}
        standard_attributes["height"] = {"value":str(50), "exec":self._setHeight}

    def _defineSpecialAttributes(self, special_attributes):
        # Interactive-Attributes
        special_attributes["onhover"] = {"value":"false"}
        special_attributes["onhoverbackgroundcolor"] = {"value":"white"}
        special_attributes["onhoverforegroundcolor"] = {"value":"black"}

        special_attributes["fontfamily"] = {"value":"Helvetica"}
        special_attributes["fontsize"] = {"value":str(12)}
        special_attributes["fontweight"] = {"value":"normal"}

    def _defineActions(self, actions):
        actions["click"] = {"policy":None, "exec":self._defineClickEvent}

    #----------------------------------------------------------------------------------------------
    #-----Standard-Attributes----
    #----------------------------------------------------------------------------------------------

    def _setLabelText(self, component, key, standard_attributes):
        text = standard_attributes[key]["value"]
        if text[0] == "\"":
            text = text[1:]
        if text[len(text)-1] == "\"":
            text = text[:-1]
        component.configure(text = text)

    def _setBackgroundColor(self, component, key, standard_attributes):
        component.configure(background = standard_attributes[key]["value"])

    def _setForegroundColor(self, component, key, standard_attributes):
        component.configure(foreground = standard_attributes[key]["value"])

    def _setWidth(self, component, key, standard_attributes):
        value = standard_attributes[key]["value"]
        if value.isdigit():
            component.configure(width = int(value))
        else:
            self._logger.warn("For element " + self._id + " ,setWidth for " + key + " is not a digit: " + value)

    def _setHeight(self, component, key, standard_attributes):
        value = standard_attributes[key]["value"]
        if value.isdigit():
            component.configure(height = int(value))
        else:
            self._logger.warn("For element " + self._id + " ,setHeight for " + key + " is not a digit: " + value)

    #----------------------------------------------------------------------------------------------
    #-----Special-Attributes----
    #----------------------------------------------------------------------------------------------

    def _execSpecialAttributes(self, elements, standard_attributes, special_attributes):
        self._setOnHover(elements, standard_attributes, special_attributes)
        self._setFont(elements, standard_attributes, special_attributes)
   
    def _setOnHover(self, elements, standard_attributes, special_attributes): 
        on_hover = special_attributes["onhover"]["value"]
        on_hover_background_color = special_attributes["onhoverbackgroundcolor"]["value"]
        on_hover_foreground_color = special_attributes["onhoverforegroundcolor"]["value"]

        if on_hover == "true":
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

    def _setFont(self, elements, standard_attributes, special_attributes):

        afont = font.Font(family=special_attributes["fontfamily"]["value"],
            size = int(special_attributes["fontsize"]["value"]), weight = special_attributes["fontweight"]["value"])
        self._component.configure(font=afont)


 
    #----------------------------------------------------------------------------------------------
    #-----Actions----
    #----------------------------------------------------------------------------------------------
       
    def _defineClickEvent(self, component, key, actions, standard_attributes, special_attributes, elements):
        if actions[key] and actions[key]["policy"]:
            def clickEvent(event):
                self._base_engine.assume(actions[key]["policy"])

            component.bind('<Button-1>', clickEvent)

    def _addComponentToElements(self, elements):
        self._component.pack(expand=True)
        elements[str(self._id)] = (self._component, {})






