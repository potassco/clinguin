import json

import networkx as nx

from typing import Sequence, Any

from server.application.element import ElementDto
from server.application.attribute import AttributeDto
from server.application.callback import CallbackDto

from server.data.standard_clingo_solver import StandardClingoSolver, ClingoWrapper

"""
Generates a ClassHierarchy which can easily be serialized
"""
class StandardJsonEncoder:

    def __init__(self):
        pass

    def encode(self, wrapper):
        elements = {}

        root = ElementDto('root', 'root', 'root')
        elements[str(root.id)] = root    

        dependency = []
        widgets_info = {}        
        for w in wrapper.getCautiousElements():
            # Skip brave-elements
            widgets_info[w.id]={'parent':w.parent,'type':w.type}
            dependency.append((w.id,w.parent))
        DG = nx.DiGraph(dependency)
        order = list(reversed(list(nx.topological_sort(DG))))

        for element_id in order:
            if str(element_id) == 'root':
                continue
            type = widgets_info[element_id]['type']
            parent = widgets_info[element_id]['parent']
            element = ElementDto(element_id ,type ,parent)


            attributes = []
            for a in wrapper.getCautiousAttributesForElementId(element_id):
                attributes.append(AttributeDto(a.id, a.key, a.value))
            element.setAttributes(attributes)


            callbacks = []
            for c in wrapper.getCautiousCallbacksForElementId(element_id):
                callbacks.append(CallbackDto(c.id, c.action, c.policy))
            element.setCallbacks(callbacks)


            elements[str(element_id)] = element
            elements[str(element.parent)].addChild(element)


        #-----------------------------------------------------------------------
        # ----- BRAVE ----
        #-----------------------------------------------------------------------

        dependency = []
        widgets_info = {}        

        for w in wrapper.getBraveElements():
            widgets_info[w.id]={'parent':w.parent,'type':w.type}
            dependency.append((w.id,w.parent))

        DG = nx.DiGraph(dependency)
        order = list(reversed(list(nx.topological_sort(DG))))

        clone = root.clone()
        elements = clone.generateTable({})

        parents = set()

        for element_id in order:
            if element_id not in widgets_info:
                continue

            element = ElementDto(element_id, widgets_info[element_id]['type'], widgets_info[element_id]['parent'])

            attributes = []
            for a in wrapper.getBraveAttributesForElementId(element_id):
                attributes.append(AttributeDto(a.id, a.key, a.value))
            element.setAttributes(attributes)


            callbacks = []
            for c in wrapper.getBraveCallbacksForElementId(element_id):
                callbacks.append(CallbackDto(c.id, c.action, c.policy))
            element.setCallbacks(callbacks)


            parents.add(str(element.parent))
            if str(element_id) not in elements:
                elements[str(element_id)] = element
                elements[str(element.parent)].addChild(element)

        for parent in parents:
            parent_elem = elements[str(parent)]
            amount = parent_elem.amountOfChildren()
            """
            print("Try: " + parent + "::" + str(amount))
            if amount == 1:
                print("Add select one")
                parent_elem.addAttribute(AttributeDto(parent, "selected", parent_elem.getChildPerIndex(0).id))
            """


        return clone





