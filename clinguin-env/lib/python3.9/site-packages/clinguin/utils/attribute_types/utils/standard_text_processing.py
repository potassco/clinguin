"""
This module contains the StandardTextProcessing class.
"""


class StandardTextProcessing:
    """
    The sole method parse_string_with_quotes removes unecessary quotes at the beginning and the end of a string.
    """

    @classmethod
    def parse_string_with_quotes(cls, text):
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
