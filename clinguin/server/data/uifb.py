# pylint: disable=R0904
"""
Module that contains the UIFB class.
"""
import logging
from pathlib import Path

import clorm
from clingo import Control
from clingo.symbol import Function, Number, String
from clorm import Raw

from clinguin.utils import Logger, NoModelError

from .attribute import AttributeDao
from .callback import CallbackDao
from .element import ElementDao


class UIFB:
    """
    The UIFB is the low-level-access-class for handling clorm and clingo,
    regarding brave-cautious and other default things.
    This class provides functionality to create a factbase with brave-cautious extended files,
    functionality to query important things for clinguin, etc.
    """

    unifiers = [ElementDao, AttributeDao, CallbackDao]

    def __init__(
        self,
        ui_files,
        constants,
        cautious_tag="_c",
        brave_tag="_b",
        auto_tag=None,
        include_menu_bar=False,
        include_unsat_msg=True,
    ):
        self._logger = logging.getLogger(Logger.server_logger_name)
        self._ui_files = ui_files
        self._tags = {"cautious": cautious_tag, "brave": brave_tag, "auto": auto_tag}
        self._conseq = {"cautious": None, "brave": None, "auto": None}
        self._factbase = None
        self._include_menu_bar = include_menu_bar
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
                    c_type
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

        existant_file_counter = 0
        for f in self._ui_files:
            path = Path(f)
            if path.is_file():
                try:
                    uictl.load(str(f))
                    existant_file_counter += 1
                except Exception:
                    self._logger.critical(
                        'Failed to load file %s (there is likely a syntax error in this logic program file).',
                        f
                    )
            else:
                self._logger.critical(
                    'File %s does not exist, this file is skipped.',
                    f
                )

        if existant_file_counter == 0:
            exception_string = (
                "None of the provided ui files exists, but at least one syntactically valid ui"
                + "file must be specified. Exiting!"
            )
            self._logger.critical(exception_string)
            raise Exception(exception_string)

        if self._include_menu_bar:
            uictl.add("base", [], UIFB.get_menu_bar_ui_encoding())
        if self._include_unsat_msg:
            uictl.add("base", [], UIFB.get_unsat_messages_ui_encoding())

        uictl.add("base", [], extra_ui_prg)
        uictl.add("base", [], self.conseq_facts)
        uictl.add("base", [], "#show element/3. #show attribute/3. #show callback/3.")
        uictl.ground([("base", [])])

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

    def set_auto_conseq(self, model_symbols):
        """
        Sets the auto conseq.
        """
        self._conseq["auto"] = model_symbols

    def get_auto_conseq(self):
        """
        Gets the auto conseq.
        """
        return self._conseq["auto"]

    def update_all_consequences(self, ctl, assumptions=None):
        """
        Updates all consequences.
        """
        c_types = ["brave", "cautious", "auto"]
        for c_type in c_types:
            try:
                self.update_consequence(c_type, ctl, assumptions)
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
                break

        self._factbase = clorm.unify(self.__class__.unifiers, model_symbols)

    def _compute_consequences(self, ctl, assumptions):
        with ctl.solve(
            assumptions=[(a, True) for a in assumptions], yield_=True
        ) as result:
            model_symbols = None
            for m in result:
                model_symbols = m.symbols(shown=True, atoms=True)

            if model_symbols is None:
                self._logger.warning("Got an UNSAT result with the given domain encoding.")
                self._unsat_core = result.core()
                raise NoModelError()

            self._unsat_core = None

        return list(model_symbols)

    def update_consequence(self, c_type, ctl, assumptions=None):
        """
        Computes for one consequence (brave/cautious/other) all consequences.
        """
        self._logger.debug("Updating %s consequences", c_type)
        if c_type in ["brave", "cautious"]:
            ctl.configuration.solve.models = 0
            ctl.configuration.solve.opt_mode = "ignore"
        else:
            ctl.configuration.solve.models = 1
            ctl.configuration.solve.opt_mode = "ignore"
        ctl.configuration.solve.enum_mode = c_type
        self._conseq[c_type] = self._compute_consequences(ctl, assumptions)

    def add_message(self, title, message, attribute_type="info"):
        """
        Adds a ''Message'' (aka. Notification/Pop-Up) for the user with a certain title and message.
        """
        self.add_element("message", "message", "window")
        self.add_attribute("message", "title", title)
        self.add_attribute("message", "message", message)
        self.add_attribute("message", "type", attribute_type)

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

    def get_elements(self):
        """
        Get all elements.
        """
        return self._factbase.query(ElementDao).all()

    def get_attributes(self):
        """
        Get all attributes.
        """
        return self._factbase.query(AttributeDao).all()

    def get_callbacks(self):
        """
        Get all callbacks.
        """
        return self._factbase.query(CallbackDao).all()

    def get_attributes_grouped(self):
        """
        Get all attributes grouped by element id.
        """
        return self._factbase.query(AttributeDao).group_by(AttributeDao.id).all()

    def get_callbacks_grouped(self):
        """
        Get all callbacks grouped by element id.
        """
        return self._factbase.query(CallbackDao).group_by(CallbackDao.id).all()

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
        return (
            self._factbase.query(CallbackDao).where(CallbackDao.id == element_id).all()
        )

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
    def get_menu_bar_ui_encoding(cls):
        """
        Get the standard lp encoding for the menu bar.
        """
        return """
element(m, menu_bar, window).
element(menu_options, menu_bar_section, m).
attribute(menu_options, label, "Options").
element(menu_options_clear, menu_bar_section_item, menu_options).
attribute(menu_options_clear, label, "Clear").
attribute(menu_options_clear, accelerator, "Cmd+C").
callback(menu_options_clear, click, clear_assumptions).
element(menu_options_next, menu_bar_section_item, menu_options).
attribute(menu_options_next, label, "Next").
attribute(menu_options_next, accelerator, "Cmd+N").
callback(menu_options_next, click, next_solution).
element(menu_options_select, menu_bar_section_item, menu_options).
attribute(menu_options_select, label, "Select").
attribute(menu_options_select, accelerator, "Cmd+S").
callback(menu_options_select, click, select)."""

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
