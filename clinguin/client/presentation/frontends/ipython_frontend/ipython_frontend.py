# pylint: disable=R0801
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

    def window(self, cid, parent, attributes, callbacks):
        print(
            "IPython - WINDOW: "
            + str(cid)
            + "::"
            + str(parent)
            + "::"
            + str(attributes)
            + "::"
            + str(callbacks)
        )

    def container(self, cid, parent, attributes, callbacks):
        print(
            "IPython - CONTAINER: "
            + str(cid)
            + "::"
            + str(parent)
            + "::"
            + str(attributes)
            + "::"
            + str(callbacks)
        )

    def dropdown_menu(self, cid, parent, attributes, callbacks):
        print(
            "IPython - DROPDOWNMENU: "
            + str(cid)
            + "::"
            + str(parent)
            + "::"
            + str(attributes)
            + "::"
            + str(callbacks)
        )

    def dropdown_menu_item(self, cid, parent, attributes, callbacks):
        print(
            "IPython - DROPDOWNMENUITEM: "
            + str(cid)
            + "::"
            + str(parent)
            + "::"
            + str(attributes)
            + "::"
            + str(callbacks)
        )

    def label(self, cid, parent, attributes, callbacks):
        print(
            "IPython - LABEL: "
            + str(cid)
            + "::"
            + str(parent)
            + "::"
            + str(attributes)
            + "::"
            + str(callbacks)
        )

    def button(self, cid, parent, attributes, callbacks):
        print(
            "IPython - BUTTON: "
            + str(cid)
            + "::"
            + str(parent)
            + "::"
            + str(attributes)
            + "::"
            + str(callbacks)
        )

    def menu_bar(self, cid, parent, attributes, callbacks):
        print(
            "IPython - MENUBAR: "
            + str(cid)
            + "::"
            + str(parent)
            + "::"
            + str(attributes)
            + "::"
            + str(callbacks)
        )

    def menu_bar_section(self, cid, parent, attributes, callbacks):
        print(
            "IPython - MENUBARSECTION: "
            + str(cid)
            + "::"
            + str(parent)
            + "::"
            + str(attributes)
            + "::"
            + str(callbacks)
        )

    def menu_bar_section_item(self, cid, parent, attributes, callbacks):
        print(
            "IPython - MENUBARSECTIONITEM: "
            + str(cid)
            + "::"
            + str(parent)
            + "::"
            + str(attributes)
            + "::"
            + str(callbacks)
        )

    def draw(self, cid):
        print("IPython - DRAW: " + str(cid))
