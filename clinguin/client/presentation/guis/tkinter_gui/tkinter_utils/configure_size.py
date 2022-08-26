from .extension_class import *

class ConfigureSize(ExtensionClass):

    @classmethod
    def getAttributes(cls, attributes = None):
        if attributes == None:
            attributes = {}

        attributes[AttributeNames.height] = {"value":0, "value_type" : IntegerType}
        attributes[AttributeNames.width] = {"value":0, "value_type" : IntegerType}

        return attributes

    def _setSize(self, elements):
        height = self._attributes[AttributeNames.height]["value"]
        width = self._attributes[AttributeNames.width]["value"]

        if height > 0 and width > 0:
            # If height is set, 
            if AttributeNames.child_layout in self._attributes:
                child_layout_value = self._attributes[AttributeNames.child_layout]["value"]

                if child_layout_value == ChildLayoutType.FLEX or child_layout_value == ChildLayoutType.RELSTATIC or child_layout_value == ChildLayoutType.ABSSTATIC:
                    self._widget.pack_propagate(0)
                elif child_layout_value == ChildLayoutType.GRID:
                    self._widget.grid_propagate(0)
            else:
                self._widget.pack_propagate(0)

        if height > 0:
            self._widget.configure(height = int(height))

        if width > 0:
            self._widget.configure(width = int(width))
    
        if height < 0:
            self._logger.warning("Height of " + self._id + " has illegal value (" + str(height) + ")")

        if width < 0:
            self._logger.warning("Width of " + self._id + " has illegal value (" + str(height) + ")")
