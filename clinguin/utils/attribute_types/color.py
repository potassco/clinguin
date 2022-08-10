import sys

from .type import Type
from .utils.standard_text_processing import StandardTextProcessing

class ColorType(Type):

    @classmethod
    def parse(cls, input: str, logger):
        parsed_string = StandardTextProcessing.parseStringWithQuotes(input)

        return parsed_string



