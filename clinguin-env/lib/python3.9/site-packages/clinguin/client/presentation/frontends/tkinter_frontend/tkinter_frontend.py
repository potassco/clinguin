"""
Contains the tkinter-gui class.
"""

import networkx as nx

from clinguin.client import AbstractFrontend
from clinguin.show_frontend_syntax_enum import ShowFrontendSyntaxEnum
from clinguin.utils.attribute_types.child_layout import ChildLayoutType
from clinguin.utils.logger import colored_text

from .tkinter_elements import (
    Button,
    Canvas,
    Container,
    Dropdownmenu,
    DropdownmenuItem,
    Label,
    MenuBar,
    MenuBarSection,
    MenuBarSectionItem,
    Message,
    RootCmp,
    Window,
)
from .tkinter_utils import AttributeNames, CallbackNames


class TkinterFrontend(AbstractFrontend):
    """
    Class that inherits from AbstractFrontend and is therefore a dynamically loaded class,
    if it shall be used to render the Frontend. It defines what to do for each element.
    """

    def __init__(self, base_engine, args):
        super().__init__(base_engine, args)

        self.elements = {}
        self.first = True

    @classmethod
    def register_options(cls, parser):
        parser.description = (
            "This GUI is based on the Python-Tkinter package and uses tkinter elements."
        )

    @classmethod
    def available_syntax(cls, show_level):
        def append_dict(description, d, type_name):
            for key in d.keys():
                description += colored_text("    " + key + "\n", "GREEN")
                if show_level == ShowFrontendSyntaxEnum.FULL:
                    if "description" in d[key]:
                        # Specific has higher priority
                        description = description + "      Description: "
                        description = description + ": " + d[key]["description"]
                        description = description + "\n"
                    elif key in AttributeNames.descriptions:
                        # General lesser priority
                        description = description + "      Description: "
                        description = (
                            description
                            + ": "
                            + colored_text(AttributeNames.descriptions[key], "MAGENTA")
                        )
                        description = description + "\n"
                    elif key in CallbackNames.descriptions:
                        description = description + "      Description: "
                        description = (
                            description
                            + ": "
                            + colored_text(CallbackNames.descriptions[key], "MAGENTA")
                        )
                        description = description + "\n"

                    if type_name in d[key]:
                        description = description + "      Possible-Values: "
                        description = description + colored_text(
                            d[key][type_name].description() + "\n", "MAGENTA"
                        )

            return description

        description = (
            "Here one finds the supported attributes and events of the TkinterFrontend "
            + "The following list shows for each the possible attributes and events."
            + "See the documentation for more details on the syntax.\n"
        )

        class_list = RootCmp.__subclasses__()

        description = description + "--------------------------------\n"
        for c in class_list:
            description = description + colored_text("" + c.__name__ + "\n", "BLUE")

            attributes = c.get_attributes()
            if len(attributes.keys()) > 0:
                description = description + colored_text("  attributes\n", "YELLOW")
                description = append_dict(description, attributes, "value_type")

            callbacks = c.get_callbacks()
            if len(callbacks.keys()) > 0:
                description = description + colored_text("  events\n", "YELLOW")
                description = append_dict(description, callbacks, "operation_type")
            description = description + "--------------------------------\n"

        return description

    def window(self, cid, parent, attributes, callbacks):
        if self.first:
            window = Window(
                self._args, cid, parent, attributes, callbacks, self._base_engine
            )
            window.add_component(self.elements)
        else:
            keys = list(self.elements.keys()).copy()
            for key in keys:
                if str(key) == str(cid):
                    continue

                if str(key) in self.elements:
                    self.elements[str(key)].forget_children(self.elements)
                    del self.elements[str(key)]

    def container(self, cid, parent, attributes, callbacks):
        container = Container(
            self._args, cid, parent, attributes, callbacks, self._base_engine
        )
        container.add_component(self.elements)

    def dropdown_menu(self, cid, parent, attributes, callbacks):
        menu = Dropdownmenu(
            self._args, cid, parent, attributes, callbacks, self._base_engine
        )
        menu.add_component(self.elements)

    def dropdown_menu_item(self, cid, parent, attributes, callbacks):
        menu = DropdownmenuItem(
            self._args, cid, parent, attributes, callbacks, self._base_engine
        )
        menu.add_component(self.elements)

    def label(self, cid, parent, attributes, callbacks):
        label = Label(self._args, cid, parent, attributes, callbacks, self._base_engine)
        label.add_component(self.elements)

    def button(self, cid, parent, attributes, callbacks):
        button = Button(
            self._args, cid, parent, attributes, callbacks, self._base_engine
        )
        button.add_component(self.elements)

    def menu_bar(self, cid, parent, attributes, callbacks):
        menubar = MenuBar(
            self._args, cid, parent, attributes, callbacks, self._base_engine
        )
        menubar.add_component(self.elements)

    def menu_bar_section(self, cid, parent, attributes, callbacks):
        menubar = MenuBarSection(
            self._args, cid, parent, attributes, callbacks, self._base_engine
        )
        menubar.add_component(self.elements)

    def menu_bar_section_item(self, cid, parent, attributes, callbacks):
        menubar = MenuBarSectionItem(
            self._args, cid, parent, attributes, callbacks, self._base_engine
        )
        menubar.add_component(self.elements)

    def message(self, cid, parent, attributes, callbacks):
        message = Message(
            self._args, cid, parent, attributes, callbacks, self._base_engine
        )
        message.add_component(self.elements)

    def canvas(self, cid, parent, attributes, callbacks):
        canvas = Canvas(
            self._args, cid, parent, attributes, callbacks, self._base_engine
        )
        canvas.add_component(self.elements)

    def draw_postprocessing(self, cid):
        self.elements[cid].get_element().update()

        elements_info = {}
        dependency = []

        for key in self.elements.keys():
            w = self.elements[key]
            if w.get_id() == "root":
                continue

            elements_info[w.get_id()] = {"parent": w.get_parent(), "type": w.get_id()}
            dependency.append((w.get_id(), w.get_parent()))

        digraph = nx.DiGraph(dependency)
        order = list((list(nx.topological_sort(digraph))))

        for element_key in order:
            if element_key == "root":
                continue

            cur_element = self.elements[element_key]

            attributes = cur_element.get_attributes_list()

            if (
                AttributeNames.height in attributes
                and AttributeNames.width in attributes
            ):
                self.postprocessing_size_setter(cid, cur_element, attributes)

    def postprocessing_size_setter(self, cid, cur_element, attributes):
        """
        Postprocessing - Used to enable setting the size and width of tkinter elemnents independent.
        Normal behavior of tkinter: Only set set the size the user wants when setting both height and width.
        Wished behavior: Also do this if only one of height or width is set.

        This is implemented here, by first analyzing which elements are drawn latest.
        Then from the latest to the first compute their actual sizes, and if necessary correct them.
        In this manner every element takes the size it has been assigned.
        """
        true_width = cur_element.get_element().winfo_width()
        true_height = cur_element.get_element().winfo_height()

        config_width = int(
            cur_element.get_attributes_list()[AttributeNames.width]["value"]
        )
        config_height = int(
            cur_element.get_attributes_list()[AttributeNames.height]["value"]
        )

        pack = False

        if config_width > 0:
            pack = True
            cur_element.get_element().config(width=config_width)
        else:
            cur_element.get_element().config(width=true_width)

        if config_height > 0:
            pack = True
            cur_element.get_element().config(height=config_height)
        else:
            cur_element.get_element().config(height=true_height)

        if pack:
            if AttributeNames.child_layout in attributes:
                operation = cur_element.get_attributes_list()[
                    AttributeNames.child_layout
                ]["value"]
                if operation == ChildLayoutType.FLEX:
                    cur_element.get_element().pack_propagate(0)
            else:
                cur_element.get_element().pack_propagate(0)

            self.elements[cid].get_element().update()

    def draw(self, cid):
        self.first = False

        self.elements[cid].get_element().mainloop()
