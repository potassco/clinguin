"""
Module that contains the CallbackDao.
"""
from clorm import Predicate, RawField


class CallbackDao(Predicate):
    """
    Class for CLORM (clingo-object-relational-mapping), i.e. for accessing callbacks in a factbase.
    """

    id = RawField
    action = RawField
    policy = RawField

    class Meta:
        """
        Meta class
        """
        name = "callback"
