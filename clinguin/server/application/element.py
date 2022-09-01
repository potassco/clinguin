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

    def setAttributes(self, attributes):
        self.attributes = attributes

    def addAttribute(self, attribute):
        self.attributes.append(attribute)

    def setCallbacks(self, callbacks):
        self.callbacks = callbacks

    def addChild(self, child):
        self.children.append(child)

    def getChildPerIndex(self, index: int):
        return self.children[0]

    def amountOfChildren(self) -> int:
        return len(self.children)

    def toJSON(self):
        return json.dumps(self, default=lambda o: str(o).__dict__)

    def clone(self):
        clone = ElementDto(self.id, self.type, self.parent)

        cloned_attributes = []
        for attribute in self.attributes:
            cloned_attributes.append(attribute.clone())
        clone.setAttributes(cloned_attributes)

        cloned_callbacks = []
        for callback in self.callbacks:
            cloned_callbacks.append(callback.clone())
        clone.setCallbacks(cloned_callbacks)

        cloned_children = []
        for child in self.children:
            cloned_children.append(child.clone())
        clone.children = cloned_children

        return clone

    def generateTable(self, table):
        table[str(self.id)] = self

        for child in self.children:
            child.generateTable(table)

        return table
