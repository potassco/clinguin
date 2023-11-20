"""
Module contains the CallbackDto class.
"""
import json


class CallbackDto:
    """
    This class represents a Callback that is Json convertible.
    Therefore objects of this class are part of the hierarchy that will get converted to Json by the
    endpoints on sending the reply.
    """

    def __init__(self, cid, event, interaction_type, policy):
        self.id = str(cid)  # pylint: disable=C0103
        self.event = str(event)
        self.interaction_type = str(interaction_type)
        self.policy = str(policy)

    def to_JSON(self):  # pylint: disable=C0103
        """
        Converts a callback dto to json.
        """
        return json.dumps(self, default=lambda o: o.__dict__)

    def clone(self):
        """
        Creates a new CallbackDto object with the same properties.
        """
        return CallbackDto(self.id, self.event, self.interaction_type, self.policy)
