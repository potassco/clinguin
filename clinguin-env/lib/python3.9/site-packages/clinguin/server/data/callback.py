# pylint: disable=R0903
"""
Module that contains the CallbackDao.
"""
from clorm import Predicate, RawField


class WhenDao(Predicate):
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
