"""
Module that contains the FlexDirectionType
"""

from enum import auto

from .enum import EnumType
from .utils.standard_text_processing import StandardTextProcessing


class FlexDirectionType(EnumType):
    """
    The FlexDirectionType is an Enum Type, which can be used to specify where a component shall
    be added relative to the parent.
    """

    COLUMN = auto()
    COLUMN_REVERSE = auto()
    ROW = auto()
    ROW_REVERSE = auto()

    @classmethod
    def parse(cls, parse_input: str, logger):
        parsed_string = (
            StandardTextProcessing.parse_string_with_quotes(parse_input)
        ).lower()

        return_value = None

        if parsed_string == cls.COLUMN.name.lower():
            return_value = cls.COLUMN
        elif parsed_string == cls.COLUMN_REVERSE.name.lower():
            return_value = cls.COLUMN_REVERSE
        elif parsed_string == cls.ROW.name.lower():
            return_value = cls.ROW
        elif parsed_string == cls.ROW_REVERSE.name.lower():
            return_value = cls.ROW_REVERSE
        else:
            logger.error(
                "Could not parse " + parsed_string + " to flex_direction type."
            )
            raise Exception(
                "Could not parse " + parsed_string + " to flex_direction type."
            )

        return return_value

    @classmethod
    def description(cls):
        return (
            "For the flex-direction type two possible values exist: column (vertical alignment)"
            + "and row (horizontal alignment)."
        )
