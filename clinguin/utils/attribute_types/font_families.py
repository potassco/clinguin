"""
Module that contains the FontFamiliesType.
"""
from enum import auto


from .utils.standard_text_processing import StandardTextProcessing
from .type import Type

class FontFamiliesType(Type):
    """
    The FontFamlies is a type, which can be used to specify the font family of a text.
    """

    @classmethod
    def parse(cls, input: str, logger):
        parsed_string = StandardTextProcessing.parseStringWithQuotes(input)

        return parsed_string


    @classmethod
    def description(cls):
        return "As the font-families change from system to system, no selection exists here. Some normal families are ''helvetica'' or ''Times'' - one has to try it, if the font is installed in once system."
