# pylint: disable=R0801
"""
Module that contains the ClingoMultishotBackend.
"""
import base64
import os
from pathlib import Path

from clingo import Control, parse_term
from clingo.script import enable_python
from clingo.symbol import Function, String
from clorm import Raw

from clinguin.server import UIFB, ClinguinBackend, StandardJsonEncoder
from clinguin.server.application.backends import ClingoBackend
from clinguin.server.data.attribute import AttributeDao
from clinguin.utils import StandardTextProcessing

enable_python()


class ClingoMultishotBackend(ClingoBackend):
    """
    The ClingoMultishotBackend class is the backend that is selected by default.
    It provides basic functionality to argue bravely and cautiously.
    Further it provides several policies for assumptions, atoms and externals.
    """

    def __init__(self, args):
        super().__init__(args)

        self._domain_files = args.domain_files
        self._ui_files = args.ui_files
        self._constants = [f"-c {v}" for v in args.const] if args.const else []

        self._init_setup()
        self._end_browsing()
        self._init_ctl()
        self._ground()

        include_unsat_msg = not args.ignore_unsat_msg
        self._uifb = UIFB(
            self._ui_files,
            self._constants,
            include_unsat_msg=include_unsat_msg,
        )

        self._encoding = "utf-8"
        self._attribute_image_key = "image"

    # ---------------------------------------------
    # Required methods
    # ---------------------------------------------

    # ---------------------------------------------
    # Private methods
    # ---------------------------------------------


    def _init_setup(self):
        """
        Initial setup of properties
        """
        super()._init_setup()
        # To make static linters happy
        self._assumptions = set()
        self._externals = {"true": set(), "false": set(), "released": set()}

    @property
    def _backend_state_prg(self):
        """
        Additional program to pass to the UI computation. It represents to the state of the backend
        """
        prg = super()._backend_state_prg
        state_prg = "#defined _clinguin_assume/1."
        for a in self._assumptions:
            state_prg += f"_clinguin_assume({str(a)})."
        return prg + state_prg

    @property
    def _output_prg(self):
        """
        Output program used when exporting into file
        """
        prg = super()._output_prg
        for a in self._assumptions:
            prg = prg + f"{str(a)}.\n"
        return prg
    
    def _solve_set_handler(self):
        self._handler = self._ctl.solve(
                assumptions=[(a, True) for a in self._assumptions], yield_=True
            )

    def _add_assumption(self, predicate_symbol):
        self._assumptions.add(predicate_symbol)

    def _update_uifb_consequences(self):
        self._uifb.update_all_consequences(self._ctl, self._assumptions, self._on_model)
        if self._uifb.is_unsat:
            self._logger.error(
                "domain files are UNSAT. Setting _clinguin_unsat to true"
            )

    # ---------------------------------------------
    # Policies
    # ---------------------------------------------

    def clear_assumptions(self):
        """
        Policy: clear_assumptions removes all assumptions, then basically ''resets'' the backend
        (i.e. it regrounds, etc.) and finally updates the model and returns the updated gui as a Json structure.
        """
        self._end_browsing()
        self._assumptions = set()

        self._update_uifb()

    def add_assumption(self, predicate):
        """
        Policy: Adds an assumption and returns the udpated Json structure.
        """
        predicate_symbol = parse_term(predicate)
        if predicate_symbol not in self._assumptions:
            self._add_assumption(predicate_symbol)
            self._end_browsing()
            self._update_uifb()

    def remove_assumption(self, predicate):
        """
        Policy: Removes an assumption and returns the udpated Json structure.
        """
        predicate_symbol = parse_term(predicate)
        if predicate_symbol in self._assumptions:
            self._assumptions.remove(predicate_symbol)
            self._end_browsing()
            self._update_uifb()

    def remove_assumption_signature(self, predicate):
        """
        Policy: removes predicates with the predicate name of predicate and the given arity
        """
        predicate_symbol = parse_term(predicate)
        arity = len(predicate_symbol.arguments)
        to_remove = []
        for s in self._assumptions:
            if s.match(predicate_symbol.name, arity):
                for i, a in enumerate(predicate_symbol.arguments):
                    if str(a) != "any" and s.arguments[i] != a:
                        break
                else:
                    to_remove.append(s)
                    continue
        for s in to_remove:
            self._assumptions.remove(s)
        if len(to_remove) > 0:
            self._end_browsing()
            self._update_uifb()


    def set_external(self, predicate, value):
        """
        Policy: Sets the value of an external.
        """
        symbol = parse_term(predicate)
        name = value
        self._end_browsing()

        if name == "release":
            self._ctl.release_external(parse_term(predicate))
            self._externals["released"].add(symbol)

            if symbol in self._externals["true"]:
                self._externals["true"].remove(symbol)

            if symbol in self._externals["false"]:
                self._externals["false"].remove(symbol)

        elif name == "true":
            self._ctl.assign_external(parse_term(predicate), True)
            self._externals["true"].add(symbol)

            if symbol in self._externals["false"]:
                self._externals["false"].remove(symbol)

        elif name == "false":
            self._ctl.assign_external(parse_term(predicate), False)
            self._externals["false"].add(symbol)

            if symbol in self._externals["true"]:
                self._externals["true"].remove(symbol)

        else:
            raise ValueError(
                f"Invalid external value {name}. Must be true, false or relase"
            )

        self._update_uifb()

    def select(self):
        """
        Policy: Select the current solution during browsing
        """
        self._end_browsing()
        last_model_symbols = self._uifb.get_auto_conseq()
        symbols_to_ignore = self._externals["true"]
        symbols_to_ignore.union(self._externals["false"])
        for s in last_model_symbols:  # pylint: disable=E1133
            if s not in symbols_to_ignore:
                self._add_assumption(s)
        self._update_uifb()
