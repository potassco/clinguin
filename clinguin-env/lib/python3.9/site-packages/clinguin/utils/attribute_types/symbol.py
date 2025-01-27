"""
This module contains the SymbolType class.
"""

import clingo

from .type import Type
from .utils.standard_text_processing import StandardTextProcessing


class SymbolType(Type):
    """
    This class checks if the input IS A symbol, it does not parse it to a symbol.
    """

    @classmethod
    def parse(cls, parse_input: str, logger) -> str:
        parsed_string = StandardTextProcessing.parse_string_with_quotes(parse_input)

        try:
            clingo.parse_term(parsed_string)
            return parsed_string
        except Exception as ex:
            error_string = "The string " + parsed_string + " is not a clingo symbol!"
            logger.error(error_string)
            raise Exception(error_string) from ex

    @classmethod
    def description(cls):
        return "Corresponds to a clingo-symbol, e.g. p(4)"
