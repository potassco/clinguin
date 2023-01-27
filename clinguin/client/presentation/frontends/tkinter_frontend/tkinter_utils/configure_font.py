"""
This module contains the ConfigureSize class.
"""
from .extension_class import *
from tkinter import font

class ConfigureFont(ExtensionClass):
    """
    If a element is a subtype of the configure-size class the size of the element can be adjusted.
    """

    def __init__(self):
        self._configure_font_element = None

    @classmethod
    def get_attributes(cls, attributes = None):
        if attributes is None:
            attributes = {}

        attributes[AttributeNames.font_family] = {"value":"", "value_type" : FontFamiliesType}
        attributes[AttributeNames.font_size] = {"value":12, "value_type" : IntegerType}
        attributes[AttributeNames.font_weight] = {"value":"normal", "value_type" : FontWeightType}

        return attributes

    def _set_font(self, elements):
    
        family = family=self._attributes[AttributeNames.font_family]["value"]
        size = int(self._attributes[AttributeNames.font_size]["value"])
        weight = self._attributes[AttributeNames.font_weight]["value"]

        kwargs = {}
        if family != "":
            kwargs["family"] = family
        if size > 0:
            kwargs["size"] = size
        
        if weight in [FontWeightType.BOLD, FontWeightType.ITALIC_BOLD]:
            kwargs["weight"] = "bold"
        if weight in [FontWeightType.ITALIC, FontWeightType.ITALIC_BOLD]:
            kwargs["slant"] = "italic"
        
        if family != "" or size != "" or weight != FontWeightType.NORMAL:
            afont = font.Font(**kwargs)
            self._configure_font_element.configure(font=afont)

