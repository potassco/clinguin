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
    def parse(cls, input: str, logger):
        parsed_string = StandardTextProcessing.parseStringWithQuotes(input)

        try:
            return int(parsed_string)
        except:
            logger.error("Could not parse string to int: " + parsed_string)
            raise Exception("Could not parse string to int: " + parsed_string)

    @classmethod
    def description(cls):
        return "Specification as an integer, can be either specified as a symbol or a string."

        
