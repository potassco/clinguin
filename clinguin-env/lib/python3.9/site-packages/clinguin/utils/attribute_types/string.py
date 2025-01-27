"""
This module contains the StringType class.
"""

from .type import Type
from .utils.standard_text_processing import StandardTextProcessing


class StringType(Type):
    """
    The StringType shall be used, when the attribute value is string like.
    """

    @classmethod
    def parse(cls, parse_input: str, logger):
        parsed_string = StandardTextProcessing.parse_string_with_quotes(parse_input)

        return parsed_string

    @classmethod
    def description(cls):
        return "String, can either be specified as a string or if it is simple as a symbol."
