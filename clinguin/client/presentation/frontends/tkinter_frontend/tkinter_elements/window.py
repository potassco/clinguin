# pylint: disable=R0801,R1716
"""
Contains the window class.
"""
import tkinter as tk

from clinguin.utils.attribute_types import ChildLayoutType, ColorType, IntegerType

from ..tkinter_utils import AttributeNames, LayoutController
from .root_cmp import RootCmp


class Window(RootCmp, LayoutController):
    """
    The window class is the top-lvl. component, therefore it MUST be used in every clinguin application!
    For available attributes see syntax definition.
    """

    def _init_element(self, elements):
        window = tk.Tk()
        window.title("Clinguin")

        return window

    @classmethod
    def _get_attributes(cls, attributes=None):
        if attributes is None:
            attributes = {}

        attributes[AttributeNames.backgroundcolor] = {
            "value": "white",
            "value_type": ColorType,
        }
        attributes[AttributeNames.width] = {"value": 0, "value_type": IntegerType}
        attributes[AttributeNames.height] = {"value": 0, "value_type": IntegerType}
        attributes[AttributeNames.pos_x] = {"value": -1, "value_type": IntegerType}
        attributes[AttributeNames.pos_y] = {"value": -1, "value_type": IntegerType}
        attributes[AttributeNames.resizable_x] = {"value": 1, "value_type": IntegerType}
        attributes[AttributeNames.resizable_y] = {"value": 1, "value_type": IntegerType}

        return attributes

    def _set_background_color(
        self, elements, key=AttributeNames.backgroundcolor
    ):  # pylint: disable=W0613
        value = self._attributes[key]["value"]
        self._element.configure(background=value)

    def _set_dimensions(self, elements):  # pylint: disable=W0613
        width = self._attributes[AttributeNames.width]["value"]
        height = self._attributes[AttributeNames.height]["value"]

        pos_x = self._attributes[AttributeNames.pos_x]["value"]
        pos_y = self._attributes[AttributeNames.pos_y]["value"]

        if height > 0 and width > 0:
            child_layout_value = self._attributes[AttributeNames.child_layout]["value"]

            if child_layout_value in (
                ChildLayoutType.FLEX,
                ChildLayoutType.RELSTATIC,
                ChildLayoutType.ABSSTATIC,
            ):
                self._element.pack_propagate(0)
            elif child_layout_value == ChildLayoutType.GRID:
                self._element.grid_propagate(0)

            if pos_x < 0:
                pos_x = int((int(self._element.winfo_screenwidth()) - int(width)) / 2)
            if pos_y < 0:
                pos_y = int((int(self._element.winfo_screenheight()) - int(height)) / 2)

            self._element.geometry(
                str(width) + "x" + str(height) + "+" + str(pos_x) + "+" + str(pos_y)
            )

        elif (height > 0 and width <= 0) or (height <= 0 and width > 0):
            self._logger.warning(
                "For the tkinter window one must set both height and width to positive values (not just one)."
            )

    def _set_resizable(self, elements):  # pylint: disable=W0613
        self._element.resizable(
            self._attributes[AttributeNames.resizable_x]["value"],
            self._attributes[AttributeNames.resizable_y]["value"],
        )

    def _add_component_to_elements(self, elements):
        elements[str(self._id)] = self
