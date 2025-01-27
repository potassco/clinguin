"""
This module contains the CallBackDefinition class.
"""


class CallBackDefinition:
    """
    Some elements use this class to define their callbacks (others just do it locally, which is the preferred method).
    """

    def __init__(self, cid, parent, click_operation, elements, callback):
        self._id = cid
        self._parent = parent
        self._click_operation = click_operation
        self._elements = elements
        self._callback = callback

    def __call__(self, *args):
        self._callback(self._id, self._parent, self._click_operation, self._elements)
