# pylint: disable=E1101
"""
This module contains the ConfigureBorder class.
"""

from clinguin.utils.attribute_types import ColorType, IntegerType

from .attribute_names import AttributeNames
from .extension_class import ExtensionClass


class ConfigureBorder(ExtensionClass):
    """
    If a element shall have a border (e.g. container), it must be a subtype of this class.
    """

    @classmethod
    def get_attributes(cls, attributes=None):
        if attributes is None:
            attributes = {}

        attributes[AttributeNames.border_width] = {
            "value": 0,
            "value_type": IntegerType,
        }
        attributes[AttributeNames.border_color] = {
            "value": "black",
            "value_type": ColorType,
        }

        return attributes

    def _set_border_width(
        self, elements, key=AttributeNames.border_width
    ):  # pylint: disable=W0613
        value = self._attributes[key]["value"]
        if value > 0:
            # Not using borderwidth as one cannot set the color of the default border
            self._element.configure(highlightthickness=int(value))
        elif value == 0:
            # Zero is perfectly fine, but it shouldn't be configured then
            pass
        else:
            self._logger.warning(
                "For element "
                + self._id
                + " ,setBorderwidth for "
                + key
                + " is lesser than 0: "
                + str(value)
            )

    def _set_border_background_color(
        self, elements, key=AttributeNames.border_color
    ):  # pylint: disable=W0613
        # Not using borderwidth as one cannot set the color of the default border
        value = self._attributes[key]["value"]
        self._element.configure(highlightbackground=value, highlightcolor=value)
