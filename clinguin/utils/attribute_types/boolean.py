"""
Module that contains the BooleanType class.
"""

from .type import Type
from .utils.standard_text_processing import StandardTextProcessing


class BooleanType(Type):
    """
    Class that resembles a boolean value in the attributes.
    """

    @classmethod
    def parse(cls, parse_input: str, logger):
        parsed_string = StandardTextProcessing.parse_string_with_quotes(parse_input)

        return_value = None

        if parsed_string.lower() == "true":
            return_value = True
        elif parsed_string.lower() == "false":
            return_value = False
        else:
            logger.error("Could not parse string to boolean: " + parsed_string)
            raise Exception("Could not parse string to boolean: " + parsed_string)

        return return_value

    @classmethod
    def description(cls):
        return (
            "For the boolean type, either true or false are allowed - either as string or as a clingo-symbol."
            + "If one provides it as a string, it is case-insensitive."
        )
