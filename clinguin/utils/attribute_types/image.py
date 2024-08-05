"""
This module contains the ImageType class.
"""

import base64

from .type import Type
from .utils.standard_text_processing import StandardTextProcessing


class ImageType(Type):
    """
    The ImageType shall be used when the image is transferred from the backend to the frontend
    via a Base64 encoded string.
    """

    @classmethod
    def parse(cls, parse_input: str, logger):
        parsed_string = StandardTextProcessing.parse_string_with_quotes(parse_input)

        try:
            image_initial_bytes = parsed_string.encode("utf-8")
            base64.b64decode(image_initial_bytes)
        except Exception as ex:
            logger.error("Sent image is not base64 encoded.")
            raise Exception("Sent image is not base64 encoded.") from ex

        return parsed_string

    @classmethod
    def description(cls):
        return "Image, needs to be a base64 encoded image, given as a string."
