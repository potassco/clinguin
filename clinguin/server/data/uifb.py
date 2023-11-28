# pylint: disable=R0904
"""
Module that contains the UIFB class.
"""
import logging
from pathlib import Path

import clorm
from clingo import Control
from clingo.symbol import Function, Number, String
from clingraph.clingo_utils import ClingraphContext
from clorm import Raw

from clinguin.utils import Logger, NoModelError

from .attribute import AttributeDao
from .callback import WhenDao
from .element import ElementDao


class UIFB:
    """
    The UIFB is the low-level-access-class for handling clorm and clingo,
    regarding brave-cautious and other default things.
    This class provides functionality to create a factbase with brave-cautious extended files,
    functionality to query important things for clinguin, etc.
    """

    unifiers = [ElementDao, AttributeDao, WhenDao]

    def __init__(
        self,
        ui_files,
        constants,
        cautious_tag="_c",
        brave_tag="_b",
        auto_tag=None,
        include_unsat_msg=True,
    ):
        self._logger = logging.getLogger(Logger.server_logger_name)
        self._ui_files = [] if ui_files is None else ui_files
        self._tags = {"cautious": cautious_tag, "brave": brave_tag, "auto": auto_tag}
        self._conseq = {"cautious": None, "brave": None, "auto": None}
        self._factbase = None
        self._include_unsat_msg = include_unsat_msg
        self._unsat_core = None
        self._constants = constants

    def __str__(self):
        s = "\nConsequences:\n==========\n"
        for k, v in self._conseq.items():
            s += f"{k} consequences: (tagged with {self._tags[k]})\n"
            s += " ".join([str(s) for s in v])  # pylint: disable=E1133
            s += "\n"
        s += "\nUI Factbase:\n=========\n"
        s += self._factbase.asp_str()
        return s

    @property
    def is_empty(self):
        """
        Checks whether the factbase is empty.
        if so return true, else false.
        """
        return self._factbase is None

    @property
    def is_unsat(self):
        """
        Checks for unsat.
        Returns boolean.
        """
        return self._unsat_core is not None

    def tag(self, symbols, tag):
        """
        TODO -> Documentation
        """
        if tag is None:
            return symbols
        tagged = []
        for s in symbols:
            tagged.append(Function(tag, [s]))
        return tagged

    @property
    def conseq_facts(self):
        """
        TODO -> Documentation
        """
        conseq_facts = ""
        for c_type, symbols in self._conseq.items():
            if symbols is None:
                # raise RuntimeError("Use update function before getting the program")
                self._logger.warning(
                    "No %s consequences were calculated. Update consequences before updating the UI.",
                    c_type,
                )
                continue
            conseq_facts += UIFB.symbols_to_facts(self.tag(symbols, self._tags[c_type]))

        return conseq_facts

    def _set_fb_symbols(self, symbols):
        self._factbase = clorm.unify(self.unifiers, symbols)

    def ui_control(self, extra_ui_prg=""):
        """
        Generates a ClingoControl Object from paths of ui files and extra parts of a logic program given by a string.
        """
        uictl = Control(["0", "--warn=none"] + self._constants)

        for f in self._ui_files:
            path = Path(f)
            if not path.is_file():
                self._logger.critical("File %s does not exist", f)
                raise Exception(f"File {f} does not exist")
            try:
                uictl.load(str(f))
            except Exception as e:
                self._logger.critical(
                    "Failed to load file %s (there is likely a syntax error in this logic program file).",
                    f,
                )
                self._logger.critical(str(e))
                raise e

        if self._include_unsat_msg:
            uictl.add("base", [], UIFB.get_unsat_messages_ui_encoding())

        uictl.add("base", [], extra_ui_prg)
        uictl.add("base", [], self.conseq_facts)
        uictl.add("base", [], "#show elem/3. #show attr/3. #show when/4.")
        uictl.ground([("base", [])], ClingraphContext)

        return uictl

    def from_ctl(self, ctl):
        """
        Solves a control object and sets the result of the answer sets as the factbase symbols.
        """
        with ctl.solve(yield_=True) as result:
            for m in result:
                model_symbols = m.symbols(shown=True, atoms=True)
                break

        return self._set_fb_symbols(symbols=model_symbols)

    def set_auto_conseq(self, model, on_model=lambda m: None):
        """
        Sets the auto conseq.
        Arguments:
            on_model: Optional callback to edit the models (Used for theory extensions)
        """
        on_model(model)
        model_symbols = model.symbols(shown=True, atoms=True)
        self._conseq["auto"] = model_symbols

    def get_auto_conseq(self):
        """
        Gets the auto conseq.
        """
        return self._conseq["auto"]

    def update_all_consequences(self, ctl, assumptions=None, on_model=lambda m: None):
        """
        Updates all consequences.
        Arguments:
            on_model: Optional callback to edit the models (Used for theory extensions)
        """
        c_types = ["brave", "cautious", "auto"]
        for c_type in c_types:
            try:
                self.update_consequence(c_type, ctl, assumptions, on_model=on_model)
            except NoModelError:
                # Error should be handled in the ui encoding
                return

    def update_ui(self, extra_ui_prg=""):
        """
        Computes the answer sets for the ui and adds the resulting facts accordingly.
        """
        self._logger.debug("Computing Ui with additional program:\n%s", extra_ui_prg)
        uictl = self.ui_control(extra_ui_prg)

        with uictl.solve(yield_=True) as result:
            for m in result:
                model_symbols = m.symbols(shown=True, atoms=True)
                # print(model_symbols)
                break

        self._factbase = clorm.unify(self.__class__.unifiers, model_symbols)

    def _compute_consequences(self, ctl, assumptions, on_model=lambda m: None):
        with ctl.solve(
            assumptions=[(a, True) for a in assumptions], yield_=True
        ) as result:
            model_symbols = None
            for m in result:
                on_model(m)
                model_symbols = m.symbols(shown=True, atoms=True)

            if model_symbols is None:
                self._logger.warning(
                    "Got an UNSAT result with the given domain encoding."
                )
                self._unsat_core = result.core()
                raise NoModelError()

            self._unsat_core = None

        return list(model_symbols)

    def update_consequence(
        self, c_type, ctl, assumptions=None, on_model=lambda m: None
    ):
        """
        Computes for one consequence (brave/cautious/other) all consequences.
        Arguments:
            on_model: Optional callback to edit the models (Used for theory extensions)
        """
        self._logger.debug("Updating %s consequences", c_type)
        if c_type in ["brave", "cautious"]:
            ctl.configuration.solve.models = 0
            ctl.configuration.solve.opt_mode = "ignore"
        else:
            ctl.configuration.solve.models = 1
            ctl.configuration.solve.opt_mode = "ignore"
        ctl.configuration.solve.enum_mode = c_type
        self._conseq[c_type] = self._compute_consequences(
            ctl, assumptions, on_model=on_model
        )

    def add_message(self, title, message, attribute_type="info"):
        """
        Adds a ''Message'' (aka. Notification/Pop-Up) for the user with a certain title and message.
        """
        mid = f"{hash(message)}"
        self.add_element(mid, "message", "window")
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

    def get_unsat_core(self):
        """
        Gets the unsat core variable.
        """
        return self._unsat_core

    @classmethod
    def symbols_to_facts(cls, symbols):
        """
        Converts a iterable symbols to a string of facts.
        """
        return "\n".join([str(s) + "." for s in symbols])

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
