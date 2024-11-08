"""
Module which contains the StandardJsonEncoder
"""

import logging

import networkx as nx

from clinguin.utils import Logger

from .attribute import AttributeDto
from .callback import CallbackDto
from .element import ElementDto


class StandardJsonEncoder:
    """
    The standrd json encoder is responsible for converting a UIState into a json hierarchy.
    """

    def __init__(self):
        pass

    @classmethod
    def encode(cls, ui_state):
        """
        Public easy to access wrapper for the _generate_hierarchy method.

        Arguments:
            ui_state : UIState
        """
        elements_dict = {}

        root = ElementDto("root", "root", "root")
        elements_dict[str(root.id)] = root

        cls._generate_hierarchy(ui_state, root, elements_dict)
        return root

    @classmethod
    def _generate_hierarchy(cls, ui_state, hierarchy_root, elements_dict):
        """
        Converts the UIState into an Json Hierarchy (which is represented by an ElementDto).
        Therefore it first gets all dependencies, then orders the elements according to the dependencies
        and then adds for each element its attributes, callbacks and children.

        Arguments:
            ui_state : UIState
            hierarchy_root : ElementDto
            elements_dict : Dict
        """
        logger = logging.getLogger(Logger.server_logger_name)

        dependency = []
        elements_info = {}

        for w in ui_state.get_elements():
            elements_info[w.id] = {"parent": w.parent, "type": w.type}
            dependency.append((w.id, w.parent))
        for w in ui_state.get_elements():
            if str(w.parent) != "root" and w.parent not in elements_info:
                msg = "Error in %s. Parent element (ID: %s) undefined."
                logger.critical(
                    msg,
                    str(w),
                    str(w.parent),
                )
                raise Exception(msg % (str(w), str(w.parent)))

        directed_graph = nx.DiGraph(dependency)
        order = list(reversed(list(nx.topological_sort(directed_graph))))

        attrs = ui_state.get_attributes_grouped()
        attrs = {a[0]: list(a[1]) for a in attrs}
        cbs = ui_state.get_callbacks_grouped()
        cbs = {a[0]: list(a[1]) for a in cbs}

        for element_id in order:
            if str(element_id) == str(hierarchy_root.id):
                continue

            if element_id not in elements_info:
                logger.critical(
                    " The ID : '%s' was used as parent in an elem/3 predicate, could not be found!",
                    str(element_id),
                )
                raise Exception(" The ID : " + str(element_id) + " could not be found!")

            element_type = elements_info[element_id]["type"]
            parent = elements_info[element_id]["parent"]
            element = ElementDto(element_id, element_type, parent)

            if element_id in attrs:
                elem_attributes = [
                    AttributeDto(a.id, a.key, a.value) for a in attrs[element_id]
                ]
                element.set_attributes(elem_attributes)
            if element_id in cbs:
                elem_callbacks = [
                    CallbackDto(a.id, a.event, a.action, a.operation)
                    for a in cbs[element_id]
                ]
                element.set_callbacks(elem_callbacks)

            elements_dict[str(element_id)] = element
            elements_dict[str(element.parent)].add_child(element)
