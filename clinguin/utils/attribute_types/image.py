import sys

from .type import Type
from .utils.standard_text_processing import StandardTextProcessing

class ImageType(Type):

    @classmethod
    def parse(cls, input: str, logger):
        parsed_string = StandardTextProcessing.parseStringWithQuotes(input)

        return parsed_string


    @classmethod
    def description(cls):
        return "Image, needs to be a base64 encoded image, given as a string."
