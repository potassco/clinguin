"""
This module contains the ColorType class.
"""

from .type import Type
from .utils.standard_text_processing import StandardTextProcessing


class ColorType(Type):
    """
    The color type is used for specifying a color.
    """

    @classmethod
    def parse(cls, parse_input: str, logger):
        parsed_string = (
            StandardTextProcessing.parse_string_with_quotes(parse_input)
        ).lower()

        return parsed_string

    @classmethod
    def description(cls):
        return (
            "One can specify the color either by providing a simple-color symbol or string"
            + "(like white, black, etc.), or by specifying it directly via a 9-digit hex-string,"
            + "where the definition of it is: '#RRRGGGBBB' where R means Red, G means Green and B means Blue."
            + "E.g. black is '#000000000', red is '#fff000000', green '#000fff000', "
            + "blue '#000000fff' and white 'fffffffff'."
        )
