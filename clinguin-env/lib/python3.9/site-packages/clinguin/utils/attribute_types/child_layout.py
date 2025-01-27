"""
Module that contains the ChildLayoutType.
"""

from enum import auto

from .enum import EnumType
from .utils.standard_text_processing import StandardTextProcessing


class ChildLayoutType(EnumType):
    """
    The ChildLayoutType is an Enum Type, which can be used to specify the layout of the children.
    """

    FLEX = auto()
    GRID = auto()
    ABSSTATIC = auto()
    RELSTATIC = auto()

    @classmethod
    def parse(cls, parse_input: str, logger):
        parsed_string = (
            StandardTextProcessing.parse_string_with_quotes(parse_input)
        ).lower()

        return_value = None

        if parsed_string == cls.FLEX.name.lower():
            return_value = cls.FLEX
        elif parsed_string == cls.GRID.name.lower():
            return_value = cls.GRID
        elif parsed_string == cls.ABSSTATIC.name.lower():
            return_value = cls.ABSSTATIC
        elif parsed_string == cls.RELSTATIC.name.lower():
            return_value = cls.RELSTATIC
        else:
            logger.error("Could not parse " + parsed_string + " to child_layout type.")
            raise Exception(
                "Could not parse " + parsed_string + " to child_layout type."
            )

        return return_value

    @classmethod
    def description(cls):
        return (
            "For the child-layout four different options exists: flex (default, tries to do it automatically),"
            + "grid (grid-like-specification), absstatic (if one wants to specify the position with absolute-pixel"
            + "coordinates) and relstatic (if one wants to specify the position with relative-pixel coordinates"
            + "(from 0 to 100 percent, where 0 means left/top and 100 means right/bottom)). They can either be"
            + "specified via a clingo symbol or via a string (string is case-insensitive)."
        )
