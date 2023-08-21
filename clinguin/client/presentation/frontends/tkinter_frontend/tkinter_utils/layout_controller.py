"""
This module contains the LayoutController class.
"""
from .extension_class import *


class LayoutController(ExtensionClass):
    """
    If a element is a subtype of this class, then it can steer the layouting behavior of children.
    """

    @classmethod
    def get_attributes(cls, attributes = None):
        if attributes is None:
            attributes = {}

        attributes[AttributeNames.child_layout] = {"value": ChildLayoutType.FLEX, "value_type" : ChildLayoutType}

        return attributes
 
    def _set_child_org(self, elements):
        value = self._attributes[AttributeNames.child_layout]["value"]
        self._child_layout = value

    def get_child_org(self):
        return self._child_layout

    def get_fit_children_size(self):
        return self._fit_children_size


