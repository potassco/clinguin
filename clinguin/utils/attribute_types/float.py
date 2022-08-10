import sys

from .type import Type
from .utils.standard_text_processing import StandardTextProcessing

class FloatType(Type):

    @classmethod
    def parse(cls, input: str, logger):
        parsed_string = StandardTextProcessing.parseStringWithQuotes(input)

        try:
            return float(parsed_string)
        except:
            logger.error("Could not parse string to float: " + parsed_string)
            raise Exception("Could not parse string to float: " + parsed_string)

