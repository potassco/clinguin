"""
Module contains the CaseConverter class.
"""


class CaseConverter:
    """
    The CaseConverter class provides functionality to convert strings from one type-case (like snake_case) to another (like camelCase).

    Methods:
        snake_case_to_camel_case(snake_case : str) -> str
    """

    @classmethod
    def snake_case_to_camel_case(cls, snake_case):
        components = snake_case.split("_")

        return components[0] + "".join(x.title() for x in components[1:])
