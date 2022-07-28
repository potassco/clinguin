import logging

class RootCmp:

    def __init__(self, args, id, parent, attributes, callbacks, base_engine):
        self._logger = logging.getLogger(args.log_args['name'])
        self._id = id
        self._parent = parent
        self._attributes = attributes
        self._callbacks = callbacks
        self._base_engine = base_engine
        self._component = None

    def addComponent(self, elements):
        self._component = self._defineComponent(elements)        

        standard_attributes = {}
        special_attributes = {}

        self._defineStandardAttributes(standard_attributes)
        self._defineSpecialAttributes(special_attributes)

        self._fillAttributes(standard_attributes, special_attributes)

        self._execStandardAttributes(standard_attributes)

        self._execSpecialAttributes(elements, special_attributes)


        actions = {}
        self._defineActions(actions)
        self._fillActions(actions)
        self._execActions(actions, standard_attributes, special_attributes, elements)

        self._addComponentToElements(elements)
    
    def _defineComponent(self, elements):
        return None

    def _defineStandardAttributes(self, standard_attributes):
        pass

    def _defineSpecialAttributes(self, special_attributes):
        pass

    def _fillAttributes(self, standard_attributes, special_attributes):
         for attribute in self._attributes:
            key = attribute['key']
            value = attribute['value']
            if key in standard_attributes and "value" in standard_attributes[key]:
                standard_attributes[key]["value"] = value
            elif key in special_attributes and "value" in special_attributes[key]:
                special_attributes[key]["value"] = value
            else:
                self._logger.warn('Undefined Command: ' + key)

    def _execStandardAttributes(self, standard_attributes):
        for attribute in standard_attributes.keys():
            standard_attributes[attribute]["exec"](self._component, attribute, standard_attributes)
                
    def _execSpecialAttributes(self, elements, complex_attributes):
        pass

    def _defineActions(self, actions):
        pass 

    def _fillActions(self, actions):
        for callback in self._callbacks:
            key = callback['action']
            value = callback['policy']
            if key in actions and "policy" in actions[key]:
                actions[key]["policy"] = value
            else:
                self._logger.warn('Undefined Command: ' + key + ", or policy item missing in command.")

    def _execActions(self, actions, standard_attributes, special_attributes, elements):
        for key in actions.keys():
            actions[key]["exec"](self._component, key, actions, standard_attributes, special_attributes, elements)
 

    def _addComponentToElements(self, elements):
        elements[str(self._id)] = (self._component, {})
    

    
