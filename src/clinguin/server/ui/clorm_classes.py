# pylint: disable=R0903
"""
Module that contains the Clorm classes for the UI.
"""
from clorm import Predicate, RawField


class Element(Predicate):
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


class Attribute(Predicate):
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


class When(Predicate):
    """
    Actions define the interactivity of the UI.  Multiple actions are allowed, as explained below.

    - id: Identifier of the element that the user interacted with.
    - event: The event that is being triggered, such as click, hover,  input, etc.
            Each element type allows different events.
    - action: The action performed.
        - call: Calls the server to perform an operation.
        - update: Updates the attribute of another element without any calls to the server.
        - context: Updates the internal context that will be passed to the server on the following call actions.
                    See Context for more details.
    - operation: The operation accounts for the information that the action requires for its execution.

    """

    # pylint: disable=abstract-method

    id = RawField
    event = RawField
    action = RawField
    operation = RawField

    class Meta:
        """
        Meta class
        """

        name = "when"
