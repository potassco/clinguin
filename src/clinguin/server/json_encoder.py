"""
Module which contains the JsonEncoder
"""

import logging
import networkx as nx
from pydantic import BaseModel
from typing import List, Dict, Any

log = logging.getLogger(__name__)


class AttributeDTO(BaseModel):
    """
    Represents an attribute in the JSON convertible hierarchy.
    """

    id: str
    key: str
    value: str


class WhenDTO(BaseModel):
    """
    Represents a WhenDTO that is JSON convertible.
    """

    id: str
    event: str
    action: str
    operation: str


class ElementDTO(BaseModel):
    """
    Represents an element that is JSON convertible.
    These components form the core of the JSON hierarchy.
    """

    id: str
    type: str
    parent: str
    attributes: List[AttributeDTO] = []
    when: List[WhenDTO] = []
    children: List["ElementDTO"] = []


class JsonEncoder:
    """
    The standard JSON encoder responsible for converting a UIState into a JSON hierarchy.
    """

    @classmethod
    def encode(cls, ui_state, ds_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Converts UIState and domain state dictionary to JSON.

        Arguments:
            ui_state: UIState
            ds_dict: Dictionary of domain state.

        Returns:
            A properly formatted JSON dictionary.
        """
        elements_dict: Dict[str, ElementDTO] = {}

        root = ElementDTO(id="root", type="root", parent="root")
        elements_dict[root.id] = root

        cls._generate_hierarchy(ui_state, root, elements_dict)

        return {"ui": root.dict(), "ds": ds_dict}  # ✅ FastAPI will handle serialization

    @classmethod
    def _generate_hierarchy(cls, ui_state, hierarchy_root: ElementDTO, elements_dict: Dict[str, ElementDTO]) -> None:
        """
        Converts UIState into a JSON hierarchy (represented by an ElementDTO).
        It first gets all dependencies, orders the elements according to dependencies,
        and then adds for each element its attributes, whens, and children.

        Arguments:
            ui_state: The UI state containing elements.
            hierarchy_root: The root of the hierarchy.
            elements_dict: Dictionary mapping element IDs to ElementDTO instances.
        """

        dependency = []
        elements_info = {}

        # Extract element dependencies
        for w in ui_state.get_elements():
            elements_info[w.id] = {"parent": w.parent, "type": w.type}
            dependency.append((w.id, w.parent))

        # Ensure all parent elements exist
        for w in ui_state.get_elements():
            if str(w.parent) != "root" and w.parent not in elements_info:
                msg = f"Error in {w}. Parent element (ID: {w.parent}) undefined."
                log.error(msg)
                raise Exception(msg)

        directed_graph = nx.DiGraph(dependency)
        order = list(reversed(list(nx.topological_sort(directed_graph))))

        attrs = ui_state.get_attributes_grouped()
        attrs = {a[0]: list(a[1]) for a in attrs}
        whens = ui_state.get_whens_grouped()
        whens = {a[0]: list(a[1]) for a in whens}

        # Construct the element hierarchy
        for element_id in order:
            if str(element_id) == str(hierarchy_root.id):
                continue

            if element_id not in elements_info:
                log.error(
                    f" The ID '{element_id}' was used as a parent in an elem/3 predicate, but could not be found!"
                )
                raise Exception(f" The ID '{element_id}' could not be found!")

            element_type = elements_info[element_id]["type"]
            parent = elements_info[element_id]["parent"]

            # 🔥 Ensure Raw objects are converted to strings
            element = ElementDTO(
                id=str(element_id),  # ✅ Convert Raw to string
                type=str(element_type),  # ✅ Convert Raw to string
                parent=str(parent),  # ✅ Convert Raw to string
            )

            if element_id in attrs:
                element.attributes = [
                    AttributeDTO(id=str(a.id), key=str(a.key), value=str(a.value)) for a in attrs[element_id]
                ]
            if element_id in whens:
                element.when = [
                    WhenDTO(id=str(w.id), event=str(w.event), action=str(w.action), operation=str(w.operation))
                    for w in whens[element_id]
                ]

            elements_dict[str(element_id)] = element
            elements_dict[str(parent)].children.append(element)
