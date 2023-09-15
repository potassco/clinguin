# pylint: disable=R0903
"""
Module that contains the CallbackDao.
"""
from clorm import Predicate, RawField


class DoDao(Predicate):
    """
    Class for CLORM (clingo-object-relational-mapping), i.e. for accessing 'do' in a factbase.
    """

    id = RawField
    action_type = RawField
    interaction_type = RawField
    policy = RawField

    class Meta:
        """
        Meta class
        """

        name = "do"
