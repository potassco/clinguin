# pylint: disable=R0903
"""
Module that contains the ElementDao.
"""
from clorm import Predicate, RawField


class ElementDao(Predicate):
    """
    Elements define building blocks of the UI.

    - id: Identifies the element for further references.
    - type: The type of element (window, container, button etc).
    - parent: The id of the parent element. The identifier root is used as the root element of the UI.

    """

    # pylint: disable=abstract-method

    id = RawField
    type = RawField
    parent = RawField

    class Meta:
        """
        Meta class
        """

        name = "elem"
