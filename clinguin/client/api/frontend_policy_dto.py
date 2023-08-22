"""
Module contains the FrontendPolicyDto class
"""
import json


class FrontendPolicyDto:
    """
    Dto class for encapsulating the json that shall be sent to the backend that handles the callbacks.
    """

    def __init__(self, function):
        self.function = function

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)
