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
    def parse(cls, input: str, logger) -> str:
        parsed_string = StandardTextProcessing.parse_string_with_quotes(input)

        try:
            clingo.parse_term(parsed_string)
            return parsed_string
        except Exception:
            error_string = "The string " + parsed_string + " is not a clingo symbol!"
            logger.error(error_string)
            raise Exception(error_string)

    @classmethod
    def description(cls):
        return "Corresponds to a clingo-symbol, e.g. p(4)"
