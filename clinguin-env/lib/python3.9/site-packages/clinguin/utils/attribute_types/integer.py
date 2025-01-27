"""
This module contains the IntegerType class.
"""

from .type import Type
from .utils.standard_text_processing import StandardTextProcessing


class IntegerType(Type):
    """
    The IntegerType shall be used, when the attribute value is integer like.
    """

    @classmethod
    def parse(cls, parse_input: str, logger):
        parsed_string = StandardTextProcessing.parse_string_with_quotes(parse_input)

        try:
            return int(parsed_string)
        except Exception as ex:
            logger.error("Could not parse string to int: " + parsed_string)
            raise Exception("Could not parse string to int: " + parsed_string) from ex

    @classmethod
    def description(cls):
        return "Specification as an integer, can be either specified as a symbol or a string."
