"""
This module contains the PathType.
"""

from os import path

from .type import Type
from .utils.standard_text_processing import StandardTextProcessing


class PathType(Type):
    """
    The PathType shall be used, when a path is specified (checks if path exists).
    """

    @classmethod
    def parse(cls, parse_input: str, logger):
        parsed_string = StandardTextProcessing.parse_string_with_quotes(parse_input)

        return_value = None

        if path.exists(parsed_string):
            return_value = parsed_string
        else:
            error_string = "Could not find specified path: " + parsed_string
            logger.error(error_string)
            raise Exception(error_string)

        return return_value

    @classmethod
    def description(cls):
        return "String, can either be specified as a string or if it is simple as a symbol."
