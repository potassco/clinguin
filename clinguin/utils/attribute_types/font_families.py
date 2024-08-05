"""
Module that contains the FontFamiliesType.
"""

from .type import Type
from .utils.standard_text_processing import StandardTextProcessing


class FontFamiliesType(Type):
    """
    The FontFamlies is a type, which can be used to specify the font family of a text.
    """

    @classmethod
    def parse(cls, parse_input: str, logger):
        parsed_string = StandardTextProcessing.parse_string_with_quotes(parse_input)

        return parsed_string

    @classmethod
    def description(cls):
        return (
            "As the font-families change from system to system, clinguin cannot provide a useful selection"
            + "of fonts here. Therefore one should search in one's favorite search engine, how to get a list"
            + "of available fonts for one's operating system. Generally one can then use the name of the"
            + "preferred font-family as the value. Some wide spread and popular font-families are"
            + "(NOTE THAT THEY MIGHT NOT WORK ON YOUR SYSTEM!!!): [''helvetica'',''times'',''arial'',''courier'']."
        )
