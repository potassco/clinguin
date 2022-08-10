from clinguin.client.presentation.abstract_gui import AbstractGui

class IPythonGui(AbstractGui):

    def __init__(self, base_engine, args):
        super().__init__(base_engine, args)
        print("IPython - __init__")

    @classmethod
    def registerOptions(cls, parser):
        parser.description = "This GUI is based on the ipython library."

    def window(self, id, parent, attributes, callbacks):
        print("IPython - WINDOW: " + str(id) + "::" + str(parent))

    def container(self, id, parent, attributes, callbacks):
        print("IPython - CONTAINER: " + str(id) + "::" + str(parent))

    def dropdownMenu(self, id, parent, attributes, callbacks):
        print("IPython - DROPDOWNMENU: " + str(id) + "::" + str(parent))

    def dropdownMenuItem(self, id, parent, attributes, callbacks):
        print("IPython - DROPDOWNMENUITEM: " + str(id) + "::" + str(parent))

    def label(self, id, parent, attributes, callbacks):
        print("IPython - LABEL: " + str(id) + "::" + str(parent))

    def button(self, id, parent, attributes, callbacks):
        print("IPython - BUTTON: " + str(id) + "::" + str(parent))

    def menuBar(self, id, parent, attributes, callbacks):
        print("IPython - MENUBAR: " + str(id) + "::" + str(parent))

    def menuBarSection(self, id, parent, attributes, callbacks):
        print("IPython - MENUBARSECTION: " + str(id) + "::" + str(parent))

    def menuBarSectionItem(self, id, parent, attributes, callbacks):
        print("IPython - MENUBARSECTIONITEM: " + str(id) + "::" + str(parent))

    def draw(self, id):
        print("IPython - DRAW: " + str(id))
