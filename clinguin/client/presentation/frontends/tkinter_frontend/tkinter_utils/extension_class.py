"""
This module contains the ExtensionClass
"""
from clinguin.utils.attribute_types import *
from .attribute_names import AttributeNames
from .callback_names import CallbackNames


class ExtensionClass:
    """
    If a class is a subtype of the ExtensionClass it resembles a set of attributes/callbacks that can be applied to elements.
    """

    @classmethod
    def get_attributes(cls, attributes=None):
        return {}

    @classmethod
    def get_callbacks(cls, attributes=None):
        return {}
