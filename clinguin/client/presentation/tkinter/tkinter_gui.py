
import tkinter as tk
from tkinter import ttk


# TODO -> Not beautiful, implement new one or create shared folder?
from clinguin.server.application.attribute import AttributeDto

from clinguin.client.presentation.abstract_gui import AbstractGui
from clinguin.client.presentation.tkinter.call_back_definition import CallBackDefinition


class TkinterGui(AbstractGui):

    def __init__(self, baseEngine, instance):
        print("Tkinter Gui")
        self.elements = {}
        self.baseEngine = baseEngine
        self._instance = instance

        self.first = True

    def window(self, id, parent, attributes, callbacks):
        #print("WINDOW: " + str(id) + "::" + str(parent))
   

        if self.first == True: 
            self._window_startup(id, parent, attributes, callbacks)
        else:
            keys = list(self.elements.keys()).copy()
            for key in keys:
                if str(key) == str(id):
                    continue
            
                self.elements[str(key)][0].pack_forget()
                del self.elements[str(key)]


    def _window_startup(self, id, parent, attributes, callbacks):
        root = tk.Tk()

        root.title("Clinguin")

        tkinter_attributes = {
            "width" : AttributeDto(id, "width", root.winfo_screenwidth()),
            "height" : AttributeDto(id, "height", root.winfo_screenheight()),
            "backgroundcolor" : AttributeDto(id, "background", "white"),
            "resizablex" : AttributeDto(id, "resizablex", 1),
            "resizabley" : AttributeDto(id, "resizabley", 1),
            }
            

        for attribute in attributes:
            if attribute['key'] in tkinter_attributes:
                tkinter_attributes[attribute['key']].value = attribute['value']
            else:
                print('Undefined Command: ' + attribute['key'])
       
         
        tka = tkinter_attributes

        geom_string = tka["width"].value + "x" + tka["height"].value + "+" + str(int(root.winfo_screenwidth()/2 - int(tka["width"].value)/2)) + "+" + str(int(root.winfo_screenheight()/2 - int(tka["height"].value)/2))
        root.geometry(geom_string)
        
        root.configure(background = tka["backgroundcolor"].value)
        root.resizable(tka['resizablex'].value,tka['resizabley'].value)
            
        self.elements[str(id)] = (root, {})

    def dropdownmenu(self, id, parent, attributes, callbacks):
        #print("DROPDOWNMENU: " + str(id) + "::" + str(parent))


 
        tkinter_attributes = {
            "width" : AttributeDto(id, "width", "1"),
            "backgroundcolor" : AttributeDto(id, "background", "red"),
            "selected" : AttributeDto(id, "variable", ""),
            "initially_selected" : AttributeDto(id, "variable", "")
            }

 
        for attribute in attributes:
            if attribute['key'] in tkinter_attributes:
                tkinter_attributes[attribute['key']].value = attribute['value']
            else:
                print('Undefined Command: ' + attribute['key'])


        variable = tk.StringVar()
        if tkinter_attributes["initially_selected"].value != "" and tkinter_attributes["selected"].value == "":
            variable = tk.StringVar()
            variable.set(tkinter_attributes["initially_selected"].value)
        elif tkinter_attributes["selected"].value != "":
            variable = tk.StringVar()
            variable.set(tkinter_attributes["selected"].value)
        
        items = []
        
        menu = ttk.OptionMenu(self.elements[parent][0], variable, *items)
        menu.pack(expand=True)
         
        tka = tkinter_attributes
            
        self.elements[str(id)] = (menu, {"variable" : variable})


    def dropdownmenuitem(self, id, parent, attributes, callbacks):
        
        tkinter_attributes = {
            "label" : AttributeDto(id, "label", id)
            }

 
        for attribute in attributes:
            if attribute['key'] in tkinter_attributes:
                tkinter_attributes[attribute['key']].value = attribute['value']
            else:
                print('Undefined Command: ' + attribute['key'])


        click_policy = None        
        for callback in callbacks:
            if callback['action'] == 'click':
                click_policy = callback['policy']
       
        tka = tkinter_attributes
       
        menu = self.elements[str(parent)][0]

        
        menu['menu'].add_command(label=tka["label"].value, command=CallBackDefinition(id, parent, click_policy, self.dropdownmenuitemClick)) 


    def container(self, id, parent, attributes, callbacks):
 
        tkinter_attributes = {
            "gridx" : AttributeDto(id, "gridx", -1),
            "gridy" : AttributeDto(id, "gridy", -1),
            "backgroundcolor" : AttributeDto(id, "backgroundcolor", "white"),
            "width" : AttributeDto(id, "width", 50),
            "height" : AttributeDto(id, "height", 50)
            }
 
        for attribute in attributes:
            if attribute['key'] in tkinter_attributes:
                tkinter_attributes[attribute['key']].value = attribute['value']
            else:
                print('Undefined Command: ' + attribute['key'])


        click_policy = None        
        for callback in callbacks:
            if callback['action'] == 'click':
                click_policy = callback['policy']
      
        container = tk.Frame(self.elements[str(parent)][0])
        
        tka = tkinter_attributes
        if int(tka["gridx"].value) >= 0 and int(tka["gridy"].value) >= 0:
            container.grid(column = int(tka["gridx"].value), row = int(tka["gridy"].value))

        container.configure(background = tka["backgroundcolor"].value)

        container.configure(width = int(tka["width"].value))
        container.configure(height = int(tka["height"].value))

        container.pack_propagate(0)

        
        self.elements[str(id)] = (container, {})



    def dropdownmenuitemClick(self, id, parent, click_policy):
        variable = self.elements[str(parent)][1]["variable"]
        variable.set(id)
        print(str(id) + "::" + str(parent) + "::" + str(click_policy))
        if (click_policy is not None):
            self.baseEngine.assume(click_policy)



    def draw(self, id):
        self.first = False
        self.elements[id][0].mainloop()

