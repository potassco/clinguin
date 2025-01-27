# pylint: disable=R1711
"""
Contains the RootCmp class.
"""
import logging

from clinguin.utils.attribute_types import ChildLayoutType, StringType, SymbolType

from ..tkinter_utils import ExtensionClass


class RootCmp:
    """
    Every tkinter element must be a subtype of the RootCmp.
    It further features standard implementations of various methods,
    therefore one must just implement a handful of methods if one implements a new element,
    these are (see e.g. the button.py for a sample implementation):
    - _get_attributes(attributes = None)
    - _get_callbacks(callbacks = None)
    - Every method, which name starts with ''_set'' will be executed and are designed to be used
    for setting the attributes.
    - Every method, which name starts with ''_define'' will be executed and are designet to specify callbacks.
    """

    def __init__(self, args, cid, parent, attributes, callbacks, base_engine):
        self._logger = logging.getLogger(args.log_args["name"])
        self._id = cid
        self._parent = parent
        self._json_attributes = attributes
        self._json_callbacks = callbacks
        self._base_engine = base_engine
        self._element = None

        self._attributes = None
        self._callbacks = None

    def get_id(self):
        """
        Get the id of the element.
        """
        return self._id

    def get_parent(self):
        """
        Get the parent of the element.
        """
        return self._parent

    def get_element(self):
        """
        Get the tkinter object of the element.
        """
        return self._element

    def get_attributes_list(self):
        """
        Get the attributes list of instance.
        """
        return self._attributes

    @classmethod
    def get_attributes(cls):
        """
        Get attributes list of class (which attributes has this class in general).
        """
        attributes = {}
        for base in cls.__bases__:
            if issubclass(base, ExtensionClass):
                base.get_attributes(attributes)

        return cls._get_attributes(attributes)

    @classmethod
    def _get_attributes(cls, attributes=None):  # pylint: disable=W0613
        return {}

    @classmethod
    def get_callbacks(cls):
        """
        Get callbacks list of class (which callbacks has this class in general).
        """
        callbacks = {}
        for base in cls.__bases__:
            if issubclass(base, ExtensionClass):
                base.get_callbacks(callbacks)

        return cls._get_callbacks(callbacks)

    @classmethod
    def _get_callbacks(cls, callbacks=None):  # pylint: disable=W0613
        return {}

    def add_component(self, elements):
        """
        Add the current (self) component to elements.
        """
        self._element = self._init_element(elements)  # pylint: disable=E1128
        self._attributes = self.__class__.get_attributes()
        self._callbacks = self.__class__.get_callbacks()

        self._fill_attributes()
        self._fill_callbacks()

        self._exec_attributes(elements)
        self._exec_actions(elements)

        self._add_component_to_elements(elements)

    def _init_element(self, elements):
        self._logger.debug(str(elements))
        return None

    def _fill_attributes(self):
        for attribute in self._json_attributes:
            key = attribute["key"]
            value = attribute["value"]
            if key in self._attributes and "value_type" in self._attributes[key]:
                value_type = self._attributes[key]["value_type"]
            else:
                value_type = StringType
            if key in self._attributes and "value" in self._attributes[key]:
                self._attributes[key]["value"] = value_type.parse(value, self._logger)
            else:
                self._logger.warning(
                    "Undefined Command: " + key + " for element: " + attribute["id"]
                )

    def _fill_callbacks(self):
        for callback in self._json_callbacks:
            if callback["action"] not in ["call", "callback"]:
                self._logger.warning(
                    "Only interaction type call and callback are available in the Tkinter frontend.\
                    Interactivity: '%s' was ignored",
                    callback["action"],
                )
            key = callback["event"]
            value = callback["operation"]
            if key in self._callbacks and "operation_type" in self._callbacks[key]:
                value_type = self._callbacks[key]["operation_type"]
            else:
                value_type = SymbolType

            if key in self._callbacks and "operation" in self._callbacks[key]:
                self._callbacks[key]["operation"] = value_type.parse(
                    value, self._logger
                )
            else:
                self._logger.warning(
                    "Undefined Command: %s, or operation item missing in command.", key
                )

    def _get_methods(self, start_string):
        object_methods = []
        for method_name in dir(self):
            if method_name.startswith(start_string) and callable(
                getattr(self, method_name)
            ):
                object_methods.append(getattr(self, method_name))

        return object_methods

    def _exec_attributes(self, elements):
        attribute_methods = self._get_methods("_set")
        for set_attribute_method in attribute_methods:
            set_attribute_method(elements)

    def _exec_actions(self, elements):
        callback_methods = self._get_methods("_define")
        for define_callback_method in callback_methods:
            define_callback_method(elements)

    def _add_component_to_elements(self, elements):
        elements[str(self._id)] = self

    def forget_children(self, elements):
        """
        The current element drops all relations to its children (thereby 'forgetting' them).
        """
        if str(self._parent) in elements:
            if hasattr(elements[self._parent], "get_child_org"):
                parent_org = getattr(elements[self._parent], "get_child_org")()
                if parent_org in (
                    ChildLayoutType.FLEX,
                    ChildLayoutType.RELSTATIC,
                    ChildLayoutType.ABSSTATIC,
                ):
                    self._element.pack_forget()
                elif parent_org == ChildLayoutType.GRID:
                    self._element.grid_forget()
                else:
                    self._element.forget()
            else:
                self._element.forget()
        else:
            pass
