"""
This module contains the StandardTextProcessing class.
"""

class StandardTextProcessing:
    """
    The sole method parseStringWithQuotes removes unecessary quotes at the beginning and the end of a string.
    """

    @classmethod
    def parseStringWithQuotes(cls, text):
        if len(text) > 0:
            if text[0] == "\"":
                text = text[1:]
        if len(text) > 0:
            if text[len(text)-1] == "\"":
                text = text[:-1]

        return text
 
