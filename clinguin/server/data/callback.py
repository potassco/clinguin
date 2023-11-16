# pylint: disable=R0903
"""
Module that contains the CallbackDao.
"""
from clorm import Predicate, RawField


class WhenDao(Predicate):
    """
    Class for CLORM (clingo-object-relational-mapping), i.e. for accessing 'when' in a factbase.
    """

    id = RawField
    event = RawField
    interaction_type = RawField
    policy = RawField

    class Meta:
        """
        Meta class
        """

        name = "when"
