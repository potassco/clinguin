"""
This module contains the Type class.
"""

class Type:
    """
    The Type class is the super class of all Clinguin-Value-Types, i.e. each individual type must be a subtype of Type.
    """

    @classmethod
    def parse(cls, input : str, logger):
        return None
    
    @classmethod
    def description(cls):
        return ""
