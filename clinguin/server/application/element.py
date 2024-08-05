"""
Module that contains the ElementDto class.
"""

import json


class ElementDto:
    """
    The class that represents elements that are Json convertible,
    i.e. these components are the heart of the Json convertible hierarchy.
    """

    def __init__(self, cid, element_type, parent):
        self.id = str(cid)  # pylint: disable=C0103
        self.type = str(element_type)
        self.parent = str(parent)
        self.attributes = []
        self.when = []
        self.children = []

    def set_attributes(self, attributes):
        """
        Sets (all) the attributes of this element.
        """
        self.attributes = attributes

    def add_attribute(self, attribute):
        """
        Adds an attribute to this element.
        """
        self.attributes.append(attribute)

    def set_callbacks(self, callbacks):
        """
        Sets (all) the callbacks of this element.
        """
        self.when = callbacks

    def to_JSON(self):  # pylint: disable=C0103
        """
        Converts the element to a json.
        """
        return json.dumps(self, default=lambda o: str(o).__dict__)

    def clone(self):
        """
        Creates a new ElementDto object with the same properties as the self object.
        Note that all attributes, callbacks and children (elements) are deep copied/cloned.
        """
        clone = ElementDto(self.id, self.type, self.parent)

        cloned_attributes = []
        for attribute in self.attributes:
            cloned_attributes.append(attribute.clone())
        clone.set_attributes(cloned_attributes)

        cloned_callbacks = []
        for callback in self.when:
            cloned_callbacks.append(callback.clone())
        clone.set_callbacks(cloned_callbacks)

        cloned_children = []
        for child in self.children:
            cloned_children.append(child.clone())
        clone.children = cloned_children

        return clone

    def add_child(self, child):
        """
        Adds a child (element) to this element.
        """
        self.children.append(child)
