"""
Contains the RootCmp class.
"""
import logging
from clinguin.utils.attribute_types import *
from ..tkinter_utils import *

class RootCmp:
    """
    Every tkinter widget must be a subtype of the RootCmp. It further features standard implementations of various methods, therefore one must just implement a handful of methods if one implements a new widget, these are (see e.g. the button.py for a sample implementation):
    - _getAttributes(attributes = None)
    - _getCallbacks(callbacks = None)
    - Every method, which name starts with ''_set'' will be executed and are designed to be used for setting the attributes.
    - Every method, which name starts with ''_define'' will be executed and are designet to specify callbacks.
    """

    def __init__(self, args, id, parent, attributes, callbacks, base_engine):
        self._logger = logging.getLogger(args.log_args['name'])
        self._id = id
        self._parent = parent
        self._json_attributes = attributes
        self._json_callbacks = callbacks
        self._base_engine = base_engine
        self._widget = None

        self._attributes = None
        self._callbacks = None

    @classmethod
    def getAttributes(cls):

        attributes = {} 
        for base in cls.__bases__:
            if issubclass(base, ExtensionClass):
                base.getAttributes(attributes)
        
        return cls._getAttributes(attributes)

    @classmethod
    def _getAttributes(cls, attributes = None):
        return {}


    @classmethod
    def getCallbacks(cls):
        callbacks = {} 
        for base in cls.__bases__:
            if issubclass(base, ExtensionClass):
                base.getCallbacks(callbacks)
        
        return cls._getCallbacks(callbacks)
    
    @classmethod
    def _getCallbacks(cls, callbacks = None):
        return {}


    def getWidget(self):
        return self._widget

    def addComponent(self, elements):
        self._widget = self._initWidget(elements)        

        self._attributes = self.__class__.getAttributes()
        self._callbacks = self.__class__.getCallbacks()

        self._fillAttributes()
        self._fillCallbacks()

        self._execAttributes(elements)
        self._execActions(elements)

        self._addComponentToElements(elements)
    
    def _initWidget(self, elements):
        return None

    def _fillAttributes(self):
        for attribute in self._json_attributes:
            key = attribute['key']
            value = attribute['value']
            if key in self._attributes and 'value_type' in self._attributes[key]:
                value_type = self._attributes[key]['value_type']
            else:
                value_type = StringType

            if key in self._attributes and "value" in self._attributes[key]:
                self._attributes[key]["value"] = value_type.parse(value, self._logger)
            else:
                self._logger.warning('Undefined Command: ' + key + ' for element: ' + attribute['id'])

    def _fillCallbacks(self):
        for callback in self._json_callbacks:
            key = callback['action']
            value = callback['policy']
            if key in self._callbacks and 'policy_type' in self._callbacks[key]:
                value_type = self._callbacks[key]['policy_type']
            else:
                value_type = SymbolType

            if key in self._callbacks and "policy" in self._callbacks[key]:
                self._callbacks[key]["policy"] = value_type.parse(value, self._logger)
            else:
                self._logger.warning('Undefined Command: %s, or policy item missing in command.', key)

    def _getMethods(self, start_string):

        object_methods = []
        for method_name in dir(self):
            if method_name.startswith(start_string) and callable(getattr(self, method_name)):
                object_methods.append(getattr(self, method_name))


        return object_methods

    def _execAttributes(self, elements):
        attribute_methods = self._getMethods("_set")

        for set_attribute_method in attribute_methods:
            set_attribute_method(elements)

    def _execActions(self, elements):
        callback_methods = self._getMethods("_define")
        for define_callback_method in callback_methods:
            define_callback_method(elements)

    def _addComponentToElements(self, elements):
        elements[str(self._id)] = self
    
    def forgetChildren(self, elements):
        if str(self._parent) in elements:
            if hasattr(elements[self._parent], "getChildOrg"):
                parent_org = getattr(elements[self._parent], "getChildOrg")()
                if parent_org in (ChildLayoutType.FLEX, ChildLayoutType.RELSTATIC, ChildLayoutType.ABSSTATIC):
                    self._widget.pack_forget()
                elif parent_org == ChildLayoutType.GRID:
                    self._widget.grid_forget()
                else:
                    self._widget.forget()
            else:
                self._widget.forget()
        else:
            pass

    
