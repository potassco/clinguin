"""
Module contains the AttributeDto class.
"""
import json


class AttributeDto:
    """
    Objects of this class represent the attributes in the json convertible hierarchy.
    """
    def __init__(self, id, key, value):
        self.id = str(id)
        self.key = str(key)
        self.value = str(value)

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def clone(self):
        return AttributeDto(self.id, self.key, self.value)
