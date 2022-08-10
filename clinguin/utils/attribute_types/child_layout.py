import sys
from enum import auto

from .utils.standard_text_processing import StandardTextProcessing
from .enum import EnumType


class ChildLayoutType(EnumType):
    FLEX = auto()
    GRID = auto()
    ABSSTATIC = auto()
    RELSTATIC = auto()

    @classmethod
    def parse(cls, input: str, logger):
        parsed_string = StandardTextProcessing.parseStringWithQuotes(input)

        if input == cls.FLEX.name.lower():
            return cls.FLEX
        elif input == cls.GRID.name.lower():
            return cls.GRID
        elif input == cls.ABSSTATIC.name.lower():
            return cls.ABSSTATIC
        elif input == cls.RELSTATIC.name.lower():
            return cls.RELSTATIC
        else:
            logger.error("Could not parse " + parsed_string + " to child_layout type.")
            raise Exception("Could not parse " + parsed_string + " to child_layout type.")
        


