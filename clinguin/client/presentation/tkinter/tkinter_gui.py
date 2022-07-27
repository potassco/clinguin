import tkinter as tk

from clinguin.client.presentation.abstract_gui import AbstractGui
from clinguin.client.presentation.tkinter.call_back_definition import CallBackDefinition


class Attribute:
    def __init__(self, id, key, value, action):
        self.id = id
        self.key = key
        self.value = value
        self.action = action


class TkinterGui(AbstractGui):

    def __init__(self, baseEngine):
        self.elements = {}
        self.baseEngine = baseEngine

        self.first = True

    def window(self, id, parent, attributes, callbacks):
        #print("WINDOW: " + str(id) + "::" + str(parent))

        if self.first:
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

        tka = {
            "width": Attribute(
                id,
                "width",
                root.winfo_screenwidth(),
                "geometry(tka['width'].value + 'x' + tka['height'].value + '+' + str(int(root.winfo_screenwidth()/2 - int(tka['width'].value)/2)) + '+' + str(int(root.winfo_screenheight()/2 - int(tka['height'].value)/2)))"),
            "height": Attribute(
                id,
                "height",
                root.winfo_screenheight(),
                "geometry(tka['width'].value + 'x' + tka['height'].value + '+' + str(int(root.winfo_screenwidth()/2 - int(tka['width'].value)/2)) + '+' + str(int(root.winfo_screenheight()/2 - int(tka['height'].value)/2)))"),
            "backgroundcolor": Attribute(
                id,
                "background",
                "white",
                "configure(background = tka['backgroundcolor'].value)"),
            "resizablex": Attribute(
                id,
                "resizablex",
                1,
                "resizable(tka['resizablex'].value,tka['resizabley'].value)"),
            "resizabley": Attribute(
                id,
                "resizabley",
                1,
                "resizable(tka['resizablex'].value,tka['resizabley'].value)"),
        }

        for attribute in attributes:
            if attribute['key'] in tka:
                tka[attribute['key']].value = attribute['value']
            else:
                print('Undefined Command: ' + attribute['key'])

        for attribute_key in tka:
            exec_string = tka[attribute_key].action
            if exec_string is not None:
                exec_string = 'root.' + exec_string
                exec(exec_string)

        self.elements[str(id)] = (root, {})

    def dropdownmenu(self, id, parent, attributes, callbacks):

        tka = {
            "width": Attribute(
                id,
                "width",
                50,
                None),
            "backgroundcolor": Attribute(
                id,
                "background",
                "white",
                "configure(background = tka['backgroundcolor'].value)"),
            "selected": Attribute(
                id,
                "variable",
                "",
                None),
            "initially_selected": Attribute(
                id,
                "variable",
                "",
                None),
        }

        for attribute in attributes:
            if attribute['key'] in tka:
                tka[attribute['key']].value = attribute['value']
            else:
                print('Undefined Command: ' + attribute['key'])

        variable = tk.StringVar()
        if tka["initially_selected"].value != "" and tka["selected"].value == "":
            variable.set(tka["initially_selected"].value)
        elif tka["selected"].value != "":
            variable.set(tka["selected"].value)

        items = []
        menu = tk.OptionMenu(self.elements[parent][0], variable, "", *items)

        for attribute_key in tka:
            exec_string = tka[attribute_key].action
            if exec_string is not None:
                exec_string = 'menu.' + exec_string
                exec(exec_string)

        menu.pack(expand=True)

        self.elements[str(id)] = (menu, {"variable": variable})

    def dropdownmenuitem(self, id, parent, attributes, callbacks):

        tka = {
            "label": Attribute(id, "label", id, None),
        }

        for attribute in attributes:
            if attribute['key'] in tka:
                tka[attribute['key']].value = attribute['value']
            else:
                print('Undefined Command: ' + attribute['key'])

        click_policy = None
        for callback in callbacks:
            if callback['action'] == 'click':
                click_policy = callback['policy']

        menu = self.elements[str(parent)][0]

        menu['menu'].add_command(
            label=tka["label"].value,
            command=CallBackDefinition(
                id,
                parent,
                click_policy,
                self.dropdownmenuitemClick))

        for attribute_key in tka:
            exec_string = tka[attribute_key].action
            if exec_string is not None:
                exec_string = "menu['menu']." + exec_string
                exec(exec_string)

    def container(self, id, parent, attributes, callbacks):

        tka = {
            "gridx": Attribute(id, "gridx", -1, None),
            "gridy": Attribute(id, "gridy", -1, None),
            "backgroundcolor": Attribute(id, "background", "white", "configure(background = tka['backgroundcolor'].value)"),
            "width": Attribute(id, "width", 50, "configure(width = int(tka['width'].value))"),
            "height": Attribute(id, "height", 50, "configure(height = int(tka['height'].value))"),
        }

        for attribute in attributes:
            if attribute['key'] in tka:
                tka[attribute['key']].value = attribute['value']
            else:
                print('Undefined Command: ' + attribute['key'])

        click_policy = None
        for callback in callbacks:
            if callback['action'] == 'click':
                click_policy = callback['policy']

        container = tk.Frame(self.elements[str(parent)][0])

        for attribute_key in tka:
            exec_string = tka[attribute_key].action
            if exec_string is not None:
                exec_string = "container." + exec_string
                exec(exec_string)

        if int(tka["gridx"].value) >= 0 and int(tka["gridy"].value) >= 0:
            container.grid(
                column=int(
                    tka["gridx"].value), row=int(
                    tka["gridy"].value))

        container.pack_propagate(0)

        self.elements[str(id)] = (container, {})

    def dropdownmenuitemClick(self, id, parent, click_policy):
        variable = self.elements[str(parent)][1]["variable"]
        variable.set(id)
        # print(str(id) + "::" + str(parent) + "::" + str(click_policy))
        if (click_policy is not None):
            self.baseEngine.assume(click_policy)

    def draw(self, id):
        self.first = False
        self.elements[id][0].mainloop()
