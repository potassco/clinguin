import sys
import base64

from .type import Type
from .utils.standard_text_processing import StandardTextProcessing

class ImageType(Type):

    @classmethod
    def parse(cls, input: str, logger):
        parsed_string = StandardTextProcessing.parseStringWithQuotes(input)

        try:
            image_initial_bytes = parsed_string.encode('utf-8')
            image_decoded = base64.b64decode(image_initial_bytes)
        except:
            logger.error("Sent image is not base64 encoded.")
            raise Exception("Sent image is not base64 encoded.")

        return parsed_string


    @classmethod
    def description(cls):
        return "Image, needs to be a base64 encoded image, given as a string."
