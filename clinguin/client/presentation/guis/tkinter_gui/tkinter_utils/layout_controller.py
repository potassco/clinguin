from .extension_class import *

class LayoutController(ExtensionClass):

    @classmethod
    def getAttributes(cls, attributes = None):
        attributes[AttributeNames.child_layout] = {"value": ChildLayoutType.FLEX, "value_type" : ChildLayoutType}
        attributes[AttributeNames.fit_children_size] = {"value": True, "value_type" : BooleanType}
 
    def _setChildOrg(self, elements):
        fit_children_size = self._attributes[AttributeNames.fit_children_size]["value"]
        value = self._attributes[AttributeNames.child_layout]["value"]

        if not fit_children_size:
            if value == ChildLayoutType.FLEX or value == ChildLayoutType.RELSTATIC or value == ChildLayoutType.ABSSTATIC:
                self._widget.pack_propagate(0)
            elif value == ChildLayoutType.GRID:
                self._widget.grid_propagate(0)

        self._fit_children_size = value
        self._child_layout = value
    

    def getChildOrg(self):
        return self._child_layout

    def getFitChildrenSize(self):
        return self._fit_children_size


