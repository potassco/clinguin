from clinguin.client.presentation.abstract_gui import AbstractGui

class IPythonGui(AbstractGui):

    def __init__(self, base_engine, args):
        super().__init__(base_engine, args)
        print("IPython - __init__")

    def window(self, id, parent, attributes, callbacks):
        print("IPython - WINDOW: " + str(id) + "::" + str(parent))

    def container(self, id, parent, attributes, callbacks):
        print("IPython - CONTAINER: " + str(id) + "::" + str(parent))

    def dropdownmenu(self, id, parent, attributes, callbacks):
        print("IPython - DROPDOWNMENU: " + str(id) + "::" + str(parent))

    def dropdownmenuitem(self, id, parent, attributes, callbacks):
        print("IPython - DROPDOWNMENUITEM: " + str(id) + "::" + str(parent))

    def label(self, id, parent, attributes, callbacks):
        print("IPython - LABEL: " + str(id) + "::" + str(parent))

    def button(self, id, parent, attributes, callbacks):
        print("IPython - BUTTON: " + str(id) + "::" + str(parent))

    def menubar(self, id, parent, attributes, callbacks):
        print("IPython - MENUBAR: " + str(id) + "::" + str(parent))

    def menubarsection(self, id, parent, attributes, callbacks):
        print("IPython - MENUBARSECTION: " + str(id) + "::" + str(parent))

    def menubarsectionitem(self, id, parent, attributes, callbacks):
        print("IPython - MENUBARSECTIONITEM: " + str(id) + "::" + str(parent))

    def draw(self, id):
        print("IPython - DRAW: " + str(id))