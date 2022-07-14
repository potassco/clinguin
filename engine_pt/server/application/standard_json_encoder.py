import json

import clingo
import clorm
import networkx as nx

from clorm import Predicate, ConstantField, RawField, Raw
from clingo import Control
from clingo.symbol import Function, Number, String
from clorm import StringField, RawField

from typing import Sequence, Any

from server.data.element import ElementDao
from server.data.attribute import AttributeDao
from server.data.callback import CallbackDao

from server.application.element import ElementDto
from server.application.attribute import AttributeDto
from server.application.callback import CallbackDto


"""
Generates a ClassHierarchy which can easily be serialized
"""
class StandardJsonEncoder:

    def __init__(self, facts):
        self.facts = facts
        self.unifiers = [ElementDao, AttributeDao, CallbackDao]

    def solve(self):

        # Get widget dependency to define creation order
        fb = clorm.parse_fact_string(self.facts, self.unifiers)


        dependency = []
        widgets_info = {}        
        for w in fb.query(ElementDao).all():
            widgets_info[w.id]={'parent':w.parent,'type':w.type}
            dependency.append((w.id,w.parent))
        DG = nx.DiGraph(dependency)
        order = list(reversed(list(nx.topological_sort(DG))))

        
        elements = {}

        root = ElementDto('root', 'root', 'root')
        elements[str(root.id)] = root    

        for element_id in order:
            if str(element_id) == 'root':
                continue
            type = widgets_info[element_id]['type']
            parent = widgets_info[element_id]['parent']
            element = ElementDto(element_id ,type ,parent)


            attributes = []
            for a in fb.query(AttributeDao).where(AttributeDao.id == element_id).all():
                attributes.append(AttributeDto(a.id, a.key, a.value))
            element.setAttributes(attributes)


            callbacks = []
            for c in fb.query(CallbackDao).where(CallbackDao.id == element_id).all():
                callbacks.append(CallbackDto(c.id, c.action, c.policy))
            element.setCallbacks(callbacks)


            elements[str(element_id)] = element
            elements[str(element.parent)].addChild(element)


        return root


    def addBraveElements(self, class_hierarchy:Any, prg:str, brave_elements:Sequence[str]) -> Any:
        fb = clorm.parse_fact_string(prg, self.unifiers)

        dependency = []
        widgets_info = {}        

        for t in brave_elements:
            for w in fb.query(ElementDao).all():
                # TODO -> More efficient Query, where one selects only ''dropdownmenuitem''
                if (str(w.type) == t):
                    widgets_info[w.id]={'parent':w.parent,'type':w.type}
                    dependency.append((w.id,w.parent))

        DG = nx.DiGraph(dependency)
        order = list(reversed(list(nx.topological_sort(DG))))

        clone = class_hierarchy.clone()
        elements = clone.generateTable({})

        parents = set()

        for element_id in order:
            if element_id not in widgets_info:
                continue

            element = ElementDto(element_id, widgets_info[element_id]['type'], widgets_info[element_id]['parent'])

            attributes = []
            for a in fb.query(AttributeDao).where(AttributeDao.id == element_id).all():
                attributes.append(AttributeDto(a.id, a.key, a.value))
            element.setAttributes(attributes)


            callbacks = []
            for c in fb.query(CallbackDao).where(CallbackDao.id == element_id).all():
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

















 
