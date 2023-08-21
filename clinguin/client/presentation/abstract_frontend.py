"""
Module that contains the class AbstractFrontend.
"""
import logging

from clinguin.utils import CustomArgs, Logger


class AbstractFrontend(CustomArgs):
    """
    Superclass from where every specialized gui class inherits from (e.g. TkinterFrontend). Defines the available elements.
    """

    def __init__(self, base_engine, args):
        self._args = args
        self._logger = logging.getLogger(Logger.client_logger_name)
        self._base_engine = base_engine

    @classmethod
    def available_syntax(cls, show_level):
        print(show_level)
        return ""

    def window(self, id, parent, attributes, callbacks):
        print(
            "WINDOW: "
            + str(id)
            + "::"
            + str(parent)
            + "::"
            + str(attributes)
            + "::"
            + str(callbacks)
        )

    def container(self, id, parent, attributes, callbacks):
        print(
            "CONTAINER: "
            + str(id)
            + "::"
            + str(parent)
            + "::"
            + str(attributes)
            + "::"
            + str(callbacks)
        )

    def dropdown_menu(self, id, parent, attributes, callbacks):
        print(
            "DROPDOWNMENU: "
            + str(id)
            + "::"
            + str(parent)
            + "::"
            + str(attributes)
            + "::"
            + str(callbacks)
        )

    def dropdown_menu_item(self, id, parent, attributes, callbacks):
        print(
            "DROPDOWNMENUITEM: "
            + str(id)
            + "::"
            + str(parent)
            + "::"
            + str(attributes)
            + "::"
            + str(callbacks)
        )

    def label(self, id, parent, attributes, callbacks):
        print(
            "LABEL: "
            + str(id)
            + "::"
            + str(parent)
            + "::"
            + str(attributes)
            + "::"
            + str(callbacks)
        )

    def button(self, id, parent, attributes, callbacks):
        print(
            "BUTTON: "
            + str(id)
            + "::"
            + str(parent)
            + "::"
            + str(attributes)
            + "::"
            + str(callbacks)
        )

    def menu_bar(self, id, parent, attributes, callbacks):
        print(
            "MENUBAR: "
            + str(id)
            + "::"
            + str(parent)
            + "::"
            + str(attributes)
            + "::"
            + str(callbacks)
        )

    def menu_bar_section(self, id, parent, attributes, callbacks):
        print(
            "MENUBARSECTION: "
            + str(id)
            + "::"
            + str(parent)
            + "::"
            + str(attributes)
            + "::"
            + str(callbacks)
        )

    def menu_bar_section_item(self, id, parent, attributes, callbacks):
        print(
            "MENUBARSECTIONITEM: "
            + str(id)
            + "::"
            + str(parent)
            + "::"
            + str(attributes)
            + "::"
            + str(callbacks)
        )

    def message(self, id, parent, attributes, callbacks):
        print(
            "MESSAGE: "
            + str(id)
            + "::"
            + str(parent)
            + "::"
            + str(attributes)
            + "::"
            + str(callbacks)
        )

    def canvas(self, id, parent, attributes, callbacks):
        print(
            "CANVAS: "
            + str(id)
            + "::"
            + str(parent)
            + "::"
            + str(attributes)
            + "::"
            + str(callbacks)
        )

    def draw_postprocessing(self, id):
        print("DRAW POSTPROCESSING")

    def draw(self, id):
        print("DRAW" + "::" + str(id))
