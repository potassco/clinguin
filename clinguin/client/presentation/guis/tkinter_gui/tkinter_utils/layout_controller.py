from .extension_class import *

class LayoutController(ExtensionClass):

    @classmethod
    def getAttributes(cls, attributes = None):
        if attributes == None:
            attributes = {}

        attributes[AttributeNames.child_layout] = {"value": ChildLayoutType.FLEX, "value_type" : ChildLayoutType}

        return attributes
 
    def _setChildOrg(self, elements):
        value = self._attributes[AttributeNames.child_layout]["value"]
        self._child_layout = value

    def getChildOrg(self):
        return self._child_layout

    def getFitChildrenSize(self):
        return self._fit_children_size


