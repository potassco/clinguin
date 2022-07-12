import json

import clingo
import clorm
import networkx as nx

from clorm import Predicate, ConstantField, RawField, Raw
from clingo import Control
from clingo.symbol import Function, Number, String

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
        q = fb.query(ElementDao)
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

            element = ElementDto(element_id, widgets_info[element_id]['type'], widgets_info[element_id]['parent'])


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
 
