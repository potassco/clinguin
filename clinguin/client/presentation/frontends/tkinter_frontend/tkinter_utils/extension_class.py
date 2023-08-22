"""
This module contains the ExtensionClass
"""


class ExtensionClass:
    """
    If a class is a subtype of the ExtensionClass it resembles a set of attributes/callbacks
    that can be applied to elements.
    """

    @classmethod
    def get_attributes(cls, attributes=None):
        return {}

    @classmethod
    def get_callbacks(cls, attributes=None):
        return {}
