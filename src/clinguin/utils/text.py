"""
This module contains utility functions for text manipulation.
"""

import base64


def parse_string_with_quotes(text: str) -> str:
    """
    Parses a string with quotes inside and returns the string without quotes.
    Additionally it correctly parses newlines to ''correct'' newlines.
    """
    if len(text) > 0:
        if text[0] == '"':
            text = text[1:]
    if len(text) > 0:
        if text[len(text) - 1] == '"':
            text = text[:-1]

    text = text.replace("\\n", "\n")

    return text


def image_to_b64(img: bytes) -> str:
    """
    Encodes an image in base 64
    """
    encoded = base64.b64encode(img)
    decoded = encoded.decode("utf-8")
    return decoded
