# pylint: disable=R0903
"""
Module that contains the AttributeDao.
"""
from clorm import Predicate, RawField


class AttributeDao(Predicate):
    """
    Attributes define the style of the UI.

    - id: Identifier of the element that the attribute will be set to.
    - key: The name of the attribute. Available attributes depend on the element type and the frontend.
    - value: The value of the attribute.
    """

    # pylint: disable=abstract-method

    id = RawField
    key = RawField
    value = RawField

    class Meta:
        """
        Meta class
        """

        name = "attr"
