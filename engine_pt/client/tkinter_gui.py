
import tkinter as tk
from tkinter import ttk

from client.abstract_gui import AbstractGui

# TODO -> Not beautiful, implement new one?
from server.application.attribute import AttributeDto


class TkinterGui(AbstractGui):

    def __init__(self, baseEngine):
        print("Tkinter Gui")
        self.root = None
        self.elements = {}
        self.baseEngine = baseEngine

    def window(self, id, parent, attributes, callbacks):
        #print("WINDOW: " + str(id) + "::" + str(parent))
    
        root = tk.Tk()

        root.title("Clinguin")


        tkinter_attributes = {
            "width" : AttributeDto(id, "width", root.winfo_screenwidth()),
            "height" : AttributeDto(id, "height", root.winfo_screenheight()),
            "backgroundcolor" : AttributeDto(id, "background", "white"),
            }
            

        for attribute in attributes:
            if attribute['key'] in tkinter_attributes:
                tkinter_attributes[attribute['key']].value = attribute['value']
            else:
                print('Undefined Command: ' + attribute['key'])
       
         
        tka = tkinter_attributes

        geom_string = tka["width"].value + "x" + tka["height"].value + "+" + str(int(root.winfo_screenwidth()/2 - int(tka["width"].value)/2)) + "+" + str(int(root.winfo_screenheight()/2 - int(tka["height"].value)/2))
        print(geom_string)
        root.geometry(geom_string)
        
        root.configure(background = tka["backgroundcolor"].value)
            
        self.elements[str(id)] = (root, {})

    def container(self, id, parent, attributes, callbacks):
        print("CONTAINER: " + str(id) + "::" + str(parent))
        
    def dropdownmenu(self, id, parent, attributes, callbacks):
        #print("DROPDOWNMENU: " + str(id) + "::" + str(parent))


        #languages = ['Python', 'JavaScript']
        items = []

        variable = tk.StringVar()
        menu = ttk.OptionMenu(self.elements[parent][0], variable, *items, command=self.dropdownmenuitemClick)
        menu.pack(expand=True)
   
 
        tkinter_attributes = {
            "width" : AttributeDto(id, "width", "100"),
            "backgroundcolor" : AttributeDto(id, "background", "white"),
            }

 
        for attribute in attributes:
            if attribute['key'] in tkinter_attributes:
                tkinter_attributes[attribute['key']].value = attribute['value']
            else:
                print('Undefined Command: ' + attribute['key'])
       
       
        tka = tkinter_attributes
        #menu.config(width=int(tka['width'].value))
            
        self.elements[str(id)] = (menu, {"variable" : variable})


    def dropdownmenuitem(self, id, parent, attributes, callbacks):
        #print("DROPDOWNMENUITEM: " + str(id) + "::" + str(parent))
        
        tkinter_attributes = {}

 
        for attribute in attributes:
            if attribute['key'] in tkinter_attributes:
                tkinter_attributes[attribute['key']].value = attribute['value']
            else:
                print('Undefined Command: ' + attribute['key'])


        click_policy = None        
        for callback in callbacks:
            if callback['action'] == 'click':
                click_policy = callback['policy']
       
       
        menu = self.elements[str(parent)][0]

        
        menu['menu'].add_command(label=id, command=Test(id, parent, click_policy, self.dropdownmenuitemClick)) 



    def dropdownmenuitemClick(self, id, parent, click_policy):
        variable = self.elements[str(parent)][1]["variable"]
        variable.set(id)
        print(str(id) + "::" + str(parent) + "::" + str(click_policy))
        if (click_policy is not None):
            self.baseEngine.assume(click_policy)



    def draw(self, id):
        self.elements[id][0].mainloop()

class Test:
    def __init__(self, id, parent, click_policy, callback):
        self._id = id
        self._parent = parent
        self._click_policy = click_policy
        self._callback = callback

    def __call__(self, *args):
        self._callback(self._id, self._parent, self._click_policy)

