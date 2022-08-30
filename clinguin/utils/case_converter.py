"""
Module contains the CaseConverter class.
"""

class CaseConverter:
    """
    The CaseConverter class provides functionality to convert strings from one type-case (like snake_case) to another (like camelCase).

    Methods:
        snakeCaseToCamelCase(snake_case : str) -> str
    """

    @classmethod
    def snakeCaseToCamelCase(cls, snake_case):
        components = snake_case.split('_')

        return components[0] + ''.join(x.title() for x in components[1:]) 


