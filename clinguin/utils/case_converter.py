"""
Module contains the CaseConverter class.
"""

import base64


class CaseConverter:
    """
    The CaseConverter class provides functionality to convert strings from one type-case
    (like snake_case) to another (like camelCase).

    Methods:
        snake_case_to_camel_case(snake_case : str) -> str
    """

    @classmethod
    def snake_case_to_camel_case(cls, snake_case):
        """
        Converts a snake case name to a camel case one.
        """
        components = snake_case.split("_")

        return components[0] + "".join(x.title() for x in components[1:])


def image_to_b64(img):
    """
    Encodes an image in base 64
    """
    encoded = base64.b64encode(img)
    decoded = encoded.decode("utf-8")
    return decoded
