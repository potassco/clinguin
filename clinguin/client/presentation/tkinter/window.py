import tkinter as tk

from .root_cmp import RootCmp

class Window(RootCmp):

    def _defineComponent(self, elements):
        window = tk.Tk()
        window.title("Clinguin")

        return window

    def _defineStandardAttributes(self, standard_attributes):
        standard_attributes["backgroundcolor"] = {"value":"white", "exec":self._backgroundColor}
        standard_attributes["width"] = {"value":str(self._component.winfo_screenwidth()), "exec":self._setDimensions}
        standard_attributes["height"] = {"value":str(self._component.winfo_screenheight()), "exec":self._setDimensions}
        standard_attributes["resizablex"] = {"value":str(1), "exec":self._setResizable}
        standard_attributes["resizabley"] = {"value":str(1), "exec":self._setResizable}
        standard_attributes["childorg"] = {"value":"grid", "exec":self._setChildOrg}

    def _backgroundColor(self, component, key, standard_attributes):
        component.configure(background=standard_attributes[key]["value"])

    def _setDimensions(self, component, key, standard_attributes):
        component.geometry(standard_attributes['width']['value'] + 'x' +
            standard_attributes['height']['value'] + '+' +
            str(int(component.winfo_screenwidth()/2 - int(standard_attributes['width']['value'])/2)) + '+' +
            str(int(component.winfo_screenheight()/2 - int(standard_attributes['height']['value'])/2)))

    def _setResizable(self, component, key, standard_attributes):
        component.resizable(standard_attributes['resizablex']['value'],standard_attributes['resizabley']['value'])

    def _setChildOrg(self, component, key, standard_attributes):
        self._child_org = standard_attributes[key]["value"]

    def _addComponentToElements(self, elements):
        elements[str(self._id)] = (self._component, {"childorg":self._child_org})


