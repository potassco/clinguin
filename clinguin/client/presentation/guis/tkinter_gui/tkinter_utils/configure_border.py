from .extension_class import *

class ConfigureBorder(ExtensionClass):

    @classmethod
    def getAttributes(cls, attributes = None):
        if attributes == None:
            attributes = {}

        attributes[AttributeNames.border_width] = {"value":0, "value_type" : IntegerType}
        attributes[AttributeNames.border_color] = {"value":"black", "value_type" : ColorType}

        return attributes

    def _setBorderWidth(self, elements, key = AttributeNames.border_width):
        value = self._attributes[key]["value"]
        if value > 0:
            # Not using borderwidth as one cannot set the color of the default border
            self._widget.configure(highlightthickness = int(value))
        elif value == 0:
            # Zero is perfectly fine, but it shouldn't be configured then
            pass
        else:
            self._logger.warning("For element " + self._id + " ,setBorderwidth for " + key + " is lesser than 0: " + str(value))

    def _setBorderBackgroundColor(self, elements, key = AttributeNames.border_color):
        # Not using borderwidth as one cannot set the color of the default border
        value = self._attributes[key]["value"]
        self._widget.configure(highlightbackground = value, highlightcolor = value)















