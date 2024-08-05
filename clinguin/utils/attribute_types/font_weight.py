"""
Module that contains the FontWeightType.
"""

import itertools
from enum import auto

from .enum import EnumType
from .utils.standard_text_processing import StandardTextProcessing


class FontWeightType(EnumType):
    """
    The FontWeightType is an Enum Type, which can be used to specify look and feel of text.
    """

    NORMAL = auto()
    ITALIC = auto()
    BOLD = auto()
    ITALIC_BOLD = auto()

    @classmethod
    def parse(cls, parse_input: str, logger):
        parsed_string = (
            StandardTextProcessing.parse_string_with_quotes(parse_input)
        ).lower()

        normals = ["n", "normal"]
        bolds = ["b", "bold"]
        italics = ["i", "italic"]

        combination = [bolds, italics]

        bolds_italic_list = []
        for p in itertools.permutations(combination, 2):
            l0 = p[0]
            l1 = p[1]
            zipped = list(zip(l0, l1))
            for l in zipped:
                bolds_italic_list.append(str(l[0]) + str(l[1]))
                bolds_italic_list.append(str(l[0]) + "_" + str(l[1]))
                bolds_italic_list.append(str(l[0]) + "-" + str(l[1]))

        return_value = None

        if parsed_string in bolds_italic_list:
            return_value = cls.ITALIC_BOLD
        elif parsed_string in bolds:
            return_value = cls.BOLD
        elif parsed_string in italics:
            return_value = cls.ITALIC
        elif parsed_string in normals:
            return_value = cls.NORMAL
        else:
            error_string = "Could not parse " + parsed_string + " to FontWeightType."
            logger.error(error_string)
            raise Exception(error_string)

        return return_value

    @classmethod
    def description(cls):
        return (
            "For the FontWeightType several different options exists - ['i' or 'italic'] for italic,"
            + "['b' or 'bold'] for bold and any permuation (with the delimiters '_', '-' and no delimiter)"
            + "of those for both italic and bolt. Further 'normal' exists for specifying normal font weight."
        )
