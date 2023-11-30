# pylint: disable=R0904
"""
Module that contains the UI State class.
"""
import logging
import os
from pathlib import Path

import clorm
from clingo import Control
from clingo.symbol import Function, Number, String
from clingraph.clingo_utils import ClingraphContext
from clorm import Raw

from clinguin.utils import StandardTextProcessing, image_to_b64

from .attribute import AttributeDao
from .callback import WhenDao
from .element import ElementDao

log = logging.getLogger("clinguin_server")


class UIState:
    """
    The UIState is the low-level-access-class for handling the facts defining the UI state
    """

    unifiers = [ElementDao, AttributeDao, WhenDao]

    def __init__(
        self,
        ui_files,
        domain_state,
        constants,
        include_unsat_msg=True,
    ):
        self._factbase = None
        self._ui_files = ui_files
        self._domain_state = domain_state
        self._constants = constants
        self._include_unsat_msg = include_unsat_msg

    def __str__(self):
        s = "\nUI Factbase:\n=========\n"
        s += self._factbase.asp_str()
        return s

    @property
    def is_empty(self):
        """
        Checks whether the factbase is empty.
        if so return true, else false.
        """
        return self._factbase is None

    def _set_fb_symbols(self, symbols):
        self._factbase = clorm.unify(self.unifiers, symbols)

    def ui_control(self):
        """
        Generates a ClingoControl Object to compute the UI state

        """
        uictl = Control(["0", "--warn=none"] + self._constants)

        for f in self._ui_files:
            path = Path(f)
            if not path.is_file():
                log.critical("File %s does not exist", f)
                raise Exception(f"File {f} does not exist")
            try:
                uictl.load(str(f))
            except Exception as e:
                log.critical(
                    "Failed to load file %s (there is likely a syntax error in this logic program file).",
                    f,
                )
                log.critical(str(e))
                raise e

        if self._include_unsat_msg:
            uictl.add("base", [], UIState.get_unsat_messages_ui_encoding())

        uictl.add("base", [], self._domain_state)
        uictl.add("base", [], "#show elem/3. #show attr/3. #show when/4.")
        uictl.ground([("base", [])], ClingraphContext)

        return uictl

    def update_ui_state(self):
        """
        Computes the answer set representing the UI state
        """
        log.debug("Computing UI state\n")
        uictl = self.ui_control()

        with uictl.solve(yield_=True) as result:
            for m in result:
                model_symbols = m.symbols(shown=True, atoms=True)
                break

        self._factbase = clorm.unify(self.__class__.unifiers, model_symbols)

    def add_message(self, title, message, attribute_type="info"):
        """
        Adds a ''Message'' (aka. Notification/Pop-Up) for the user with a certain title and message.
        """
        windows = list(
            self._factbase.query(ElementDao)
            .where(ElementDao.type == Raw(Function("window", [])))
            .all()
        )
        if len(windows) == 0:
            raise ValueError(
                "No window found to add message. Make sure an element of type window appears in your UI"
            )
        mid = f"{hash(message)}"
        self.add_element(mid, "message", windows[0].symbol.arguments[0])
        self.add_attribute(mid, "title", title)
        self.add_attribute(mid, "message", message)
        self.add_attribute(mid, "type", attribute_type)

    # Manage factbase

    def add_element(self, cid, t, parent):
        """
        Adds an element to the factbase.
        """
        if isinstance(cid, str):
            cid = Function(cid, [])
        if isinstance(t, str):
            t = Function(t, [])
        if isinstance(parent, str):
            parent = Function(parent, [])
        self._factbase.add(ElementDao(Raw(cid), Raw(t), Raw(parent)))

    def add_attribute(self, cid, key, value):
        """
        Adds an attribute to the factbase.
        """
        if isinstance(cid, str):
            cid = Function(cid, [])
        if isinstance(key, str):
            key = Function(key, [])
        if isinstance(value, str):
            value = String(value)
        if isinstance(value, int):
            value = Number(value)
        self._factbase.add(AttributeDao(Raw(cid), Raw(key), Raw(value)))

    def add_attribute_direct(self, new_attribute):
        """
        Directly adds an attribute.
        """
        self._factbase.add(new_attribute)

    def get_elements(self):
        """
        Get all elements.
        """
        return self._factbase.query(ElementDao).all()

    def get_attributes(self, key=None):
        """
        Get all attributes.
        """
        q = self._factbase.query(AttributeDao)
        if key is not None:
            q.where(AttributeDao.key == key)
        return q.all()

    def get_callbacks(self):
        """
        Get all callbacks.
        """
        return self._factbase.query(WhenDao).all()

    def get_attributes_grouped(self):
        """
        Get all attributes grouped by element id.
        """
        return self._factbase.query(AttributeDao).group_by(AttributeDao.id).all()

    def get_callbacks_grouped(self):
        """
        Get all callbacks grouped by element id.
        """
        return self._factbase.query(WhenDao).group_by(WhenDao.id).all()

    def get_attributes_for_element_id(self, element_id):
        """
        Get all attributes for one element id.
        """
        return (
            self._factbase.query(AttributeDao)
            .where(AttributeDao.id == element_id)
            .all()
        )

    def get_callbacks_for_element_id(self, element_id):
        """
        Get all callbacks for one element id.
        """
        return self._factbase.query(WhenDao).where(WhenDao.id == element_id).all()

    def replace_attribute(self, old_attribute, new_attribute):
        """
        Replaces the old_attribute with the new_attribute.
        """
        self._factbase.remove(old_attribute)
        self._factbase.add(new_attribute)

    @classmethod
    def symbols_to_facts(cls, symbols):
        """
        Converts a iterable symbols to a string of facts.
        """
        return "\n".join([str(s) + "." for s in symbols])

    def replace_images_with_b64(self, image_attribute_key="image"):
        """
        Replaces all images in the ui-state by b64
        """
        attributes = list(self.get_attributes())
        for attribute in attributes:
            if str(attribute.key) != image_attribute_key:
                continue

            attribute_value = StandardTextProcessing.parse_string_with_quotes(
                str(attribute.value)
            )

            if os.path.isfile(attribute_value):
                with open(attribute_value, "rb") as image_file:
                    encoded_string = image_to_b64(image_file.read())
                    new_attribute = AttributeDao(
                        Raw(Function(str(attribute.id), [])),
                        Raw(Function(str(attribute.key), [])),
                        Raw(String(str(encoded_string))),
                    )
                    self.replace_attribute(attribute, new_attribute)

    @classmethod
    def get_unsat_messages_ui_encoding(cls):
        """
        Get the standard unsat encoding for error messages.
        """
        return """
element(message_unsat,message,window):-_clinguin_unsat.
attribute(message_unsat,title,"Error"):-_clinguin_unsat.
attribute(message_unsat,message,"Unsatisfiable output."):-_clinguin_unsat.
attribute(message_unsat,type,error):-_clinguin_unsat.
"""
