"""
Module that contains the PopupTypesType.
"""
from enum import auto

from .utils.standard_text_processing import StandardTextProcessing
from .enum import EnumType

class PopupTypesType(EnumType):
    """
    The PopupType is an Enum Type, which can be used to specify look and feel of the message box.
    """

    INFO = auto()
    WARNING = auto()
    ERROR = auto()

    @classmethod
    def parse(cls, input: str, logger):
        parsed_string = (StandardTextProcessing.parse_string_with_quotes(input)).lower()

        if parsed_string == cls.INFO.name.lower():
            return cls.INFO
        elif parsed_string == cls.WARNING.name.lower():
            return cls.WARNING
        elif parsed_string == cls.ERROR.name.lower():
            return cls.ERROR
        else:
            error_string = "Could not parse " + parsed_string + " to PopupTypesType."
            logger.error(error_string)
            raise Exception(error_string)

    @classmethod
    def description(cls):
        return "For the popup-types three different options exists: ''info'' (Default information message), ''warning'' and ''error''"

