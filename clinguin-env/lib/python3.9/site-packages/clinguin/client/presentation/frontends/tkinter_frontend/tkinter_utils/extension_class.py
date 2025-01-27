"""
This module contains the ExtensionClass
"""


class ExtensionClass:
    """
    If a class is a subtype of the ExtensionClass it resembles a set of attributes/callbacks
    that can be applied to elements.
    """

    @classmethod
    def get_attributes(cls, attributes=None):  # pylint: disable=W0613
        """
        Has to be implemented by children.
        """
        return {}

    @classmethod
    def get_callbacks(cls, attributes=None):  # pylint: disable=W0613
        """
        Has to be implemented by children.
        """
        return {}
