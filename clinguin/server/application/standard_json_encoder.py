import json
import sys

import networkx as nx

from typing import Sequence, Any

from .element import ElementDto
from .attribute import AttributeDto
from .callback import CallbackDto

import logging
from clinguin.utils import Logger

"""
Generates a ClassHierarchy which can easily be serialized
"""
class StandardJsonEncoder:

    def __init__(self):
        pass

    @classmethod
    def encode(cls, model):
        logger = logging.getLogger(Logger.server_logger_name)
        elements_dict = {}

        root = ElementDto('root', 'root', 'root')
        elements_dict[str(root.id)] = root

        cls._generateHierarchy(model, root, elements_dict)

        return root

    @classmethod
    def _generateHierarchy(cls, model, hierarchy_root, elements_dict):
        logger = logging.getLogger(Logger.server_logger_name)

        dependency = []
        widgets_info = {}

        for w in model.getElements():
            widgets_info[w.id] = {'parent': w.parent, 'type': w.type}
            dependency.append((w.id, w.parent))

        DG = nx.DiGraph(dependency)
        order = list(reversed(list(nx.topological_sort(DG))))

        attrs = model.getAttributesGrouped()
        attrs = {a[0]:list(a[1]) for a in attrs}
        cbs = model.getCallbacksGrouped()
        cbs = {a[0]:list(a[1]) for a in cbs}

        for element_id in order:
            if str(element_id) == 'root':
                continue

            if not element_id in widgets_info:
                logger.fatal("The provided element id (ID : " + str(element_id) + ") could not be found!")
                raise Exception("The provided element id (ID : " + str(element_id) + ") could not be found!")

            type = widgets_info[element_id]['type']
            parent = widgets_info[element_id]['parent']
            element = ElementDto(element_id, type, parent)

            if element_id in attrs:
                elem_attributes = [AttributeDto(a.id, a.key, a.value) for a in attrs[element_id]]
                element.setAttributes(elem_attributes)
            if element_id in cbs:
                elem_callbacks = [CallbackDto(a.id, a.action, a.policy) for a in cbs[element_id]]
                element.setCallbacks(elem_callbacks)

            elements_dict[str(element_id)] = element
            elements_dict[str(element.parent)].addChild(element)
