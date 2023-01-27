"""
Module contains the CallbackDto class.
"""
import json


class CallbackDto:
    """
    This class represents a Callback that is Json convertible. Therefore objects of this class are part of the hierarchy that will get converted to Json by the endpoints on sending the reply.
    """
    def __init__(self, id, action, policy):
        self.id = str(id)
        self.action = str(action)
        self.policy = str(policy)

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def clone(self):
        return CallbackDto(self.id, self.action, self.policy)
