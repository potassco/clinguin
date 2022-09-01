"""
This module contains the ExtensionClass
"""
from clinguin.utils.attribute_types import *
from .attribute_names import AttributeNames
from .callback_names import CallbackNames

class ExtensionClass:
    """
    If a class is a subtype of the ExtensionClass it resembles a set of attributes/callbacks that can be applied to widgets.
    """

    @classmethod
    def getAttributes(cls, attributes = None):
        return {}

    @classmethod
    def getCallbacks(cls, attributes = None):
        return {}

