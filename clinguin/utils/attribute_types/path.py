import sys

from os import path

from .type import Type
from .utils.standard_text_processing import StandardTextProcessing

class PathType(Type):

    @classmethod
    def parse(cls, input: str, logger):
        parsed_string = StandardTextProcessing.parseStringWithQuotes(input)
        
        if path.exists(parsed_string):
            return parsed_string
        else:
            error_string = "Could not find specified path: " + parsed_string
            logger.error(error_string)
            raise Exception(error_string)

    @classmethod
    def description(cls):
        return "String, can either be specified as a string or if it is simple as a symbol."
