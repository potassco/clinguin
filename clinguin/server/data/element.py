# pylint: disable=R0903
"""
Module that contains the ElementDao.
"""
from clorm import Predicate, RawField


class ElementDao(Predicate):
    """
    Class for CLORM (clingo-object-relational-mapping), i.e. for accessing elements in a factbase.
    """

    id = RawField
    type = RawField
    parent = RawField

    class Meta:
        """
        Meta class
        """

        name = "elem"
