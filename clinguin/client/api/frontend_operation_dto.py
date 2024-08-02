"""
Module contains the FrontendOperationDto class
"""

import json


class FrontendOperationDto:
    """
    Dto class for encapsulating the json that shall be sent to the backend that handles the callbacks.
    """

    def __init__(self, function):
        self.function = function

    def to_JSON(self):  # pylint: disable=C0103
        """
        Converts DTO (self) to JSON.
        """
        return json.dumps(self, default=lambda o: o.__dict__)
