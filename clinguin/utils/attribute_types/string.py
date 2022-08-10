import sys

from .type import Type
from .utils.standard_text_processing import StandardTextProcessing

class StringType(Type):

    @classmethod
    def parse(cls, input: str, logger):
        parsed_string = StandardTextProcessing.parseStringWithQuotes(input)

        return parsed_string


    @classmethod
    def description(cls):
        return "String, can either be specified as a string or if it is simple as a symbol."
