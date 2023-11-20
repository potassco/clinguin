# pylint: disable=R0903
"""
Module that contains the AttributeDao.
"""
from clorm import Predicate, RawField


class AttributeDao(Predicate):
    """
    Class for CLORM (clingo-object-relational-mapping), i.e. for accessing attributes in a factbase.
    """

    id = RawField
    key = RawField
    value = RawField

    class Meta:
        """
        Meta class
        """

        name = "attr"
