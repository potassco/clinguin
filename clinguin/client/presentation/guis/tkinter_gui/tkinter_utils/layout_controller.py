from .extension_class import *

class LayoutController(ExtensionClass):

    @classmethod
    def getAttributes(cls, attributes = None):
        attributes[AttributeNames.child_layout] = {"value": ChildLayoutType.FLEX, "value_type" : ChildLayoutType}
 
    def _setChildOrg(self, elements):
        value = self._attributes[AttributeNames.child_layout]["value"]

        if value == ChildLayoutType.FLEX or value == ChildLayoutType.RELSTATIC or value == ChildLayoutType.ABSSTATIC:
            self._widget.pack_propagate(0)
        elif value == ChildLayoutType.GRID:
            self._widget.grid_propagate(0)
        else:
            self._logger.warn("For element " + self._id + " ,for the children-organisation (arg:  " + key + "), the value " + value + " is not a valid option")

        self._child_layout = value
    

    def getChildOrg(self):
        return self._child_layout


