from clinguin.utils.attribute_types import *
from .attribute_names import AttributeNames
from .callback_names import CallbackNames

class ExtensionClass:

    @classmethod
    def getAttributes(cls, attributes = None):
        return {}

    @classmethod
    def getCallbacks(cls, attributes = None):
        return {}

