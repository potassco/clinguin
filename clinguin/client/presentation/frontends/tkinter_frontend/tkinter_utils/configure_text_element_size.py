# pylint: disable=E1101,R0801
"""
This module contains the ConfigureTextElementSize class.
"""
from tkinter import font

from clinguin.utils.attribute_types import IntegerType

from .attribute_names import AttributeNames
from .extension_class import ExtensionClass


class ConfigureTextElementSize(ExtensionClass):
    """
    If a element is a subtype of the configure-element-size class the size of the element can be adjusted.
    It is required that any subtype of this type has the ''_configure_text_element_size'' variable
    (and must be set appropriately). Further any subtype MUST also be a subtype of ''configure_font''
    """

    def __init__(self):
        self._configure_text_element_size = None

    @classmethod
    def get_attributes(cls, attributes=None):
        if attributes is None:
            attributes = {}

        attributes[AttributeNames.height] = {"value": 0, "value_type": IntegerType}
        attributes[AttributeNames.width] = {"value": 0, "value_type": IntegerType}

        return attributes

    def _set_size(self, elements):  # pylint: disable=W0613
        height = self._attributes[AttributeNames.height]["value"]
        width = self._attributes[AttributeNames.width]["value"]

        self._element.pack_propagate(0)

        used_font = self._configure_text_element_size["font"]  # pylint: disable=E1136
        afont = font.Font(
            family=used_font, size=self._attributes[AttributeNames.font_size]["value"]
        )
        text = self._attributes[AttributeNames.label]["value"]

        splits = text.split("\n")

        if width == 0:
            longest_line = max(splits, key=len)
            width = afont.measure(longest_line)  # Get width of text in pixels

        if height == 0:
            number_lines = len(splits)
            single_line_height = afont.metrics("linespace")  # Get height of one line
            height = number_lines * single_line_height

        if height > 0:
            self._element.configure(height=int(height))

        if width > 0:
            self._element.configure(width=int(width))

        if height < 0:
            self._logger.warning(
                "Height of " + self._id + " has illegal value (" + str(height) + ")"
            )

        if width < 0:
            self._logger.warning(
                "Width of " + self._id + " has illegal value (" + str(height) + ")"
            )
