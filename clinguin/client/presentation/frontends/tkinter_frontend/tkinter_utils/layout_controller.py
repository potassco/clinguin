# pylint: disable=E1101
"""
This module contains the LayoutController class.
"""

from clinguin.utils.attribute_types import ChildLayoutType

from .attribute_names import AttributeNames
from .extension_class import ExtensionClass


class LayoutController(ExtensionClass):
    """
    If a element is a subtype of this class, then it can steer the layouting behavior of children.
    """

    def __init__(self):
        self._child_layout = None

    @classmethod
    def get_attributes(cls, attributes=None):
        if attributes is None:
            attributes = {}

        attributes[AttributeNames.child_layout] = {
            "value": ChildLayoutType.FLEX,
            "value_type": ChildLayoutType,
        }

        return attributes

    def _set_child_org(self, elements):  # pylint: disable=W0613
        value = self._attributes[AttributeNames.child_layout]["value"]
        self._child_layout = value

    def get_child_org(self):
        """
        Returns which child layout is used.
        """
        return self._child_layout

    def get_fit_children_size(self):
        """
        Returns the variable associated with ''if fit to children size''.
        """
        return self._fit_children_size
