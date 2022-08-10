import sys

from .type import Type
from .utils.standard_text_processing import StandardTextProcessing

class BooleanType(Type):

    @classmethod
    def parse(cls, input: str, logger):
        parsed_string = StandardTextProcessing.parseStringWithQuotes(input)

        if parsed_string.lower() == "true":
            return True
        elif parsed_string.lower() == "false":
            return False
        else:
            logger.error("Could not parse string to boolean: " + parsed_string)
            raise Exception("Could not parse string to boolean: " + parsed_string)
            


    @classmethod
    def description(cls):
        return "For the boolean type, either true or false are allowed - either as string or as a clingo-symbol. If one provides it as a string, it is case-insensitive."     
