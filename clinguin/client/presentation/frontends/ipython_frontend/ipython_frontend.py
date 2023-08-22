"""
Module that contains the IPythonFrontendClass
"""
from clinguin.client.presentation.abstract_frontend import AbstractFrontend


class IPythonFrontend(AbstractFrontend):
    """
    Not yet implemented!
    """

    def __init__(self, base_engine, args):
        super().__init__(base_engine, args)
        print("IPython - __init__")

    @classmethod
    def register_options(cls, parser):
        parser.description = "This GUI is based on the ipython library."

    def window(self, id, parent, attributes, callbacks):
        print("IPython - WINDOW: " + str(id) + "::" + str(parent))

    def container(self, id, parent, attributes, callbacks):
        print("IPython - CONTAINER: " + str(id) + "::" + str(parent))

    def dropdown_menu(self, id, parent, attributes, callbacks):
        print("IPython - DROPDOWNMENU: " + str(id) + "::" + str(parent))

    def dropdown_menu_item(self, id, parent, attributes, callbacks):
        print("IPython - DROPDOWNMENUITEM: " + str(id) + "::" + str(parent))

    def label(self, id, parent, attributes, callbacks):
        print("IPython - LABEL: " + str(id) + "::" + str(parent))

    def button(self, id, parent, attributes, callbacks):
        print("IPython - BUTTON: " + str(id) + "::" + str(parent))

    def menu_bar(self, id, parent, attributes, callbacks):
        print("IPython - MENUBAR: " + str(id) + "::" + str(parent))

    def menu_bar_section(self, id, parent, attributes, callbacks):
        print("IPython - MENUBARSECTION: " + str(id) + "::" + str(parent))

    def menu_bar_section_item(self, id, parent, attributes, callbacks):
        print("IPython - MENUBARSECTIONITEM: " + str(id) + "::" + str(parent))

    def draw(self, id):
        print("IPython - DRAW: " + str(id))
