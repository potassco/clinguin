import json

import networkx as nx

from typing import Sequence, Any

from clinguin.server.application.element import ElementDto
from clinguin.server.application.attribute import AttributeDto
from clinguin.server.application.callback import CallbackDto

"""
Generates a ClassHierarchy which can easily be serialized
"""
class StandardJsonEncoder:

    def __init__(self):
        pass

    @classmethod
    def encode(ctl, model):
        elements_dict = {}

        root = ElementDto('root', 'root', 'root')
        elements_dict[str(root.id)] = root    

        ctl._generateHierarchy(model, root, elements_dict)
        #self._generateHierarchy(wrapper.brave_wrapper, root, elements_dict)

        return root

    @classmethod
    def _generateHierarchy(ctl, wrapper, hierarchy_root, elements_dict):

        dependency = []
        widgets_info = {}        

        for w in wrapper.getElements():
            widgets_info[w.id]={'parent':w.parent,'type':w.type}
            dependency.append((w.id,w.parent))

        DG = nx.DiGraph(dependency)
        order = list(reversed(list(nx.topological_sort(DG))))

        for element_id in order:
            if element_id in widgets_info and str(element_id) != 'root':
                type = widgets_info[element_id]['type']
                parent = widgets_info[element_id]['parent']
                element = ElementDto(element_id, type, parent)

                attributes = []
                for a in wrapper.getAttributesForElementId(element_id):
                    attributes.append(AttributeDto(a.id, a.key, a.value))
                element.setAttributes(attributes)


                callbacks = []
                for c in wrapper.getCallbacksForElementId(element_id):
                    callbacks.append(CallbackDto(c.id, c.action, c.policy))
                element.setCallbacks(callbacks)

                elements_dict[str(element_id)] = element
                elements_dict[str(element.parent)].addChild(element)




