"""
Module that contains the ElementDto class.
"""
import json


class ElementDto:
    """
    The class that represents elements that are Json convertible, i.e. these components are the heart of the Json convertible hierarchy.
    """

    def __init__(self, id, type, parent):
        self.id = str(id)
        self.type = str(type)
        self.parent = str(parent)
        self.attributes = []
        self.callbacks = []
        self.children = []

    def set_attributes(self, attributes):
        self.attributes = attributes

    def add_attribute(self, attribute):
        self.attributes.append(attribute)

    def set_callbacks(self, callbacks):
        self.callbacks = callbacks

    def add_child(self, child):
        self.children.append(child)

    def get_child_per_index(self, index: int):
        return self.children[0]

    def amount_of_children(self) -> int:
        return len(self.children)

    def to_JSON(self):
        return json.dumps(self, default=lambda o: str(o).__dict__)

    def clone(self):
        clone = ElementDto(self.id, self.type, self.parent)

        cloned_attributes = []
        for attribute in self.attributes:
            cloned_attributes.append(attribute.clone())
        clone.set_attributes(cloned_attributes)

        cloned_callbacks = []
        for callback in self.callbacks:
            cloned_callbacks.append(callback.clone())
        clone.set_callbacks(cloned_callbacks)

        cloned_children = []
        for child in self.children:
            cloned_children.append(child.clone())
        clone.children = cloned_children

        return clone

    def generate_table(self, table):
        table[str(self.id)] = self

        for child in self.children:
            child.generate_table(table)

        return table
