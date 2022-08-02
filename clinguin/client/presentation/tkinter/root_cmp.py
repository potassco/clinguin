import logging

class RootCmp:

    def __init__(self, args, id, parent, attributes, callbacks, base_engine):
        self._logger = logging.getLogger(args.log_args['name'])
        self._id = id
        self._parent = parent
        self._json_attributes = attributes
        self._json_callbacks = callbacks
        self._base_engine = base_engine
        self._widget = None

    @classmethod
    def getAttributes(cls):
        return {}

    @classmethod
    def getCallbacks(cls):
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

            if key in self._attributes and "value" in self._attributes[key]:
                self._attributes[key]["value"] = value
            else:
                self._logger.warn('Undefined Command: ' + key + ' for element: ' + attribute['id'])

    def _fillCallbacks(self):
        for callback in self._json_callbacks:
            key = callback['action']
            value = callback['policy']

            if key in self._callbacks and "policy" in self._callbacks[key]:
                self._callbacks[key]["policy"] = value
            else:
                self._logger.warn('Undefined Command: ' + key + ", or policy item missing in command.")

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
                if parent_org == "flex" or parent_org == "absstatic" or parent_org =="relstatic":
                    self._widget.pack_forget()
                elif parent == "grid":
                    self._widget.grid_forget()
                else:
                    self._widget.forget()
            else:
                self._widget.forget()
        else:
            pass

    
