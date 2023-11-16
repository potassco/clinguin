# pylint: disable=R0801
"""
Module that contains the class AbstractFrontend.
"""
import logging

from clinguin.utils import CustomArgs, Logger


class AbstractFrontend(CustomArgs):
    """
    Superclass from where every specialized frontend inherits from.
    This class defines the available elements.
    """

    def __init__(self, base_engine, args):
        self._args = args
        self._logger = logging.getLogger(Logger.client_logger_name)
        self._base_engine = base_engine

    @classmethod
    def available_syntax(cls, show_level):
        """
        Shows the available syntax for the chosen frontend.
        """
        print(show_level)
        return ""

    def window(self, cid, parent, attributes, callbacks):
        """
        Window placeholder.
        """
        print(
            "WINDOW: "
            + str(cid)
            + "::"
            + str(parent)
            + "::"
            + str(attributes)
            + "::"
            + str(callbacks)
        )

    def container(self, cid, parent, attributes, callbacks):
        """
        Container placeholder.
        """
        print(
            "CONTAINER: "
            + str(cid)
            + "::"
            + str(parent)
            + "::"
            + str(attributes)
            + "::"
            + str(callbacks)
        )

    def dropdown_menu(self, cid, parent, attributes, callbacks):
        """
        Dropdown-Menu placeholder.
        """
        print(
            "DROPDOWNMENU: "
            + str(cid)
            + "::"
            + str(parent)
            + "::"
            + str(attributes)
            + "::"
            + str(callbacks)
        )

    def dropdown_menu_item(self, cid, parent, attributes, callbacks):
        """
        Dropdown-menu-item placeholder.
        """
        print(
            "DROPDOWNMENUITEM: "
            + str(cid)
            + "::"
            + str(parent)
            + "::"
            + str(attributes)
            + "::"
            + str(callbacks)
        )

    def label(self, cid, parent, attributes, callbacks):
        """
        Label placeholder.
        """
        print(
            "LABEL: "
            + str(cid)
            + "::"
            + str(parent)
            + "::"
            + str(attributes)
            + "::"
            + str(callbacks)
        )

    def button(self, cid, parent, attributes, callbacks):
        """
        Button placeholder.
        """
        print(
            "BUTTON: "
            + str(cid)
            + "::"
            + str(parent)
            + "::"
            + str(attributes)
            + "::"
            + str(callbacks)
        )

    def menu_bar(self, cid, parent, attributes, callbacks):
        """
        Menu-Bar placeholder.
        """
        print(
            "MENUBAR: "
            + str(cid)
            + "::"
            + str(parent)
            + "::"
            + str(attributes)
            + "::"
            + str(callbacks)
        )

    def menu_bar_section(self, cid, parent, attributes, callbacks):
        """
        Menu-Bar-Section placeholder.
        """
        print(
            "MENUBARSECTION: "
            + str(cid)
            + "::"
            + str(parent)
            + "::"
            + str(attributes)
            + "::"
            + str(callbacks)
        )

    def menu_bar_section_item(self, cid, parent, attributes, callbacks):
        """
        Menu-Bar-Section-item placeholder.
        """
        print(
            "MENUBARSECTIONITEM: "
            + str(cid)
            + "::"
            + str(parent)
            + "::"
            + str(attributes)
            + "::"
            + str(callbacks)
        )

    def message(self, cid, parent, attributes, callbacks):
        """
        Message placeholder.
        """
        print(
            "MESSAGE: "
            + str(cid)
            + "::"
            + str(parent)
            + "::"
            + str(attributes)
            + "::"
            + str(callbacks)
        )

    def canvas(self, cid, parent, attributes, callbacks):
        """
        Canvas placeholder.
        """
        print(
            "CANVAS: "
            + str(cid)
            + "::"
            + str(parent)
            + "::"
            + str(attributes)
            + "::"
            + str(callbacks)
        )

    def draw_postprocessing(self, cid):
        """
        Draw postprocessing placeholder.
        """
        print("DRAW POSTPROCESSING" + "::" + str(cid))

    def draw(self, cid):
        """
        Draw placeholder.
        """
        print("DRAW" + "::" + str(cid))
