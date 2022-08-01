import tkinter as tk

from clinguin.client.presentation.tkinter.root_cmp import RootCmp
from clinguin.client.presentation.tkinter.standard_text_processing import StandardTextProcessing

class MenuBarSection(RootCmp):

    def _defineComponent(self, elements):
        menubar_widget = elements[self._parent].getWidget()

        menubar_section = tk.Menu(menubar_widget)
        
        return menubar_section

    def _defineSpecialAttributes(self, special_attributes):
        special_attributes["label"] = {"value":"default_label"}
        
    def _execSpecialAttributes(self, elements, standard_attributes, special_attributes):
        self._addCascade(elements, standard_attributes, special_attributes)
 

    def _addCascade(self, elements, standard_attributes, special_attributes):
        value = special_attributes["label"]["value"]

        text = StandardTextProcessing.parseStringWithQuotes(value)

        menubar_widget = elements[self._parent].getWidget()
        menubar_widget.add_cascade(label=text, menu=self._component)
        
    def _addComponentToElements(self, elements):
       
        elements[str(self._id)] = self





