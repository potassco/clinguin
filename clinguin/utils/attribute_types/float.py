"""
This module contains the FloatType class.
"""

from .type import Type
from .utils.standard_text_processing import StandardTextProcessing


class FloatType(Type):
    """
    The flaot type shall be used, when the attribute-value is float like.
    """

    @classmethod
    def parse(cls, parse_input: str, logger):
        parsed_string = StandardTextProcessing.parse_string_with_quotes(parse_input)

        try:
            return float(parsed_string)
        except Exception as ex:
            logger.error("Could not parse string to float: " + parsed_string)
            raise Exception("Could not parse string to float: " + parsed_string) from ex

    @classmethod
    def description(cls):
        return 'Is a float type. A float must be specified as a string (e.g. "5.98").'
