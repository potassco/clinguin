import logging

from clinguin.utils import CustomArgs, Logger
from clinguin.show_gui_syntax_enum import ShowGuiSyntaxEnum

class AbstractGui(CustomArgs):

    def __init__(self, base_engine, args):
        self._args = args
        self._logger = logging.getLogger(Logger.client_logger_name)
        self._base_engine = base_engine


    @classmethod
    def availableSyntax(cls, show_level):
        return ""

    def window(self, id, parent, attributes, callbacks):
        print("WINDOW: " + str(id) + "::" + str(parent))

    def container(self, id, parent, attributes, callbacks):
        print("CONTAINER: " + str(id) + "::" + str(parent))

    def dropdownMenu(self, id, parent, attributes, callbacks):
        print("DROPDOWNMENU: " + str(id) + "::" + str(parent))

    def dropdownMenuItem(self, id, parent, attributes, callbacks):
        print("DROPDOWNMENUITEM: " + str(id) + "::" + str(parent))

    def label(self, id, parent, attributes, callbacks):
        print("LABEL: " + str(id) + "::" + str(parent))

    def button(self, id, parent, attributes, callbacks):
        print("BUTTON: " + str(id) + "::" + str(parent))

    def menuBar(self, id, parent, attributes, callbacks):
        print("MENUBAR: " + str(id) + "::" + str(parent))

    def menuBarSection(self, id, parent, attributes, callbacks):
        print("MENUBARSECTION: " + str(id) + "::" + str(parent))

    def menuBarSectionItem(self, id, parent, attributes, callbacks):
        print("MENUBARSECTIONITEM: " + str(id) + "::" + str(parent))

    def message(self, id, parent, attributes, callbacks):
        print("MESSAGE: " + str(id) + "::" + str(parent))

    def canvas(self, id, parent, attributes, callbacks):
        print("CANVAS: " + str(id) + "::" + str(parent))

    def draw(self, id):
        print("DRAW")
