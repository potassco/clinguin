# pylint: disable=E1101,R0801
"""
This module contains the ConfigureSize class.
"""

from clinguin.utils.attribute_types import ChildLayoutType, IntegerType

from .attribute_names import AttributeNames
from .extension_class import ExtensionClass


class ConfigureSize(ExtensionClass):
    """
    If a element is a subtype of the configure-size class the size of the element can be adjusted.
    """

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

        if height > 0 and width > 0:
            if AttributeNames.child_layout in self._attributes:
                child_layout_value = self._attributes[AttributeNames.child_layout][
                    "value"
                ]

                if child_layout_value in (
                    ChildLayoutType.FLEX,
                    ChildLayoutType.RELSTATIC,
                    ChildLayoutType.ABSSTATIC,
                ):
                    self._element.pack_propagate(0)
                elif child_layout_value == ChildLayoutType.GRID:
                    self._element.grid_propagate(0)
            else:
                self._element.pack_propagate(0)

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
