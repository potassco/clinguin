"""
This module contains the Type class.
"""


class Type:
    """
    The Type class is the super class of all Clinguin-Value-Types, i.e. each individual type
    must be a subtype of Type.
    """

    @classmethod
    def parse(cls, parse_input: str, logger):  # pylint: disable=W0613
        """
        Every type must override this method. This method parses/checks the given value.
        """
        return None

    @classmethod
    def description(cls):
        """
        Every type must override this method. One provides a textual description of available values
        in the return string.
        """
        return ""
