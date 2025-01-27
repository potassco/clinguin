"""
Module contains the AttributeDto class.
"""

import json


class AttributeDto:
    """
    Objects of this class represent the attributes in the json convertible hierarchy.
    """

    def __init__(self, cid, key, value):
        self.id = str(cid)  # pylint: disable=C0103
        self.key = str(key)
        self.value = str(value)

    def to_JSON(self):  # pylint: disable=C0103
        """
        Converts the object (self) to a json representation.
        """
        return json.dumps(self, default=lambda o: o.__dict__)

    def clone(self):
        """
        Creates a new AttributeDto object with the same properties.
        """
        return AttributeDto(self.id, self.key, self.value)
