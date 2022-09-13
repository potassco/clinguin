"""
Module that contains the Explanation Backend.
"""

from re import A
from clingo.symbol import Function, Number
from clingo import parse_term
from clingo.script import enable_python

# Self defined
from clinguin.server import ClinguinModel
from clinguin.server.application.default_backends.clingo_backend import ClingoBackend
from clinguin.server.application.default_backends.standard_utils.brave_cautious_helper import *
from clinguin.utils import NoModelError

enable_python()

from abc import ABC, abstractmethod
from itertools import chain, combinations


ASSUMPTION_SIGNATURE = "assume"
INITIAL_SIGNATURE = "initial"
SHOWN_SIGNATURES = ["solution", "initial"]


class ExplanationBackend(ClingoBackend):
    """
    TODO -> Add documentation!
    """

    def __init__(self, args):
        self._muc=None
        self._lit2symbol = {}
        self._mc_base_assumptions = set()
        self._last_prg = None
        super().__init__(args)
        for s in self._ctl.symbolic_atoms:
            if s.symbol.match('initial',3):
                self._mc_base_assumptions.add(s.symbol)
                self._add_symbol_to_dict(s.symbol)
        self._assumptions = self._mc_base_assumptions.copy()
    
    def _add_symbol_to_dict(self,symbol):
        lit = self._ctl.symbolic_atoms[symbol].literal
        self._lit2symbol[lit]=symbol


    def add_assumption(self, predicate):
        symbol = parse_term(predicate)
        if symbol not in self._assumptions:
            self._add_symbol_to_dict(symbol)
            self._assumptions.add(symbol)
            self._end_browsing()
            self._update_model()
        return self.get()

    def clear_assumptions(self):
        self._end_browsing()
        self._assumptions = self._mc_base_assumptions.copy()
        self._init_ctl()
        self._ground()
        self._update_model()
        return self.get()

    def _solve_core(self, assumptions):
        with self._ctl.solve(assumptions=[(a,True) for a in assumptions], yield_=True) as solve_handle:
            satisfiable = solve_handle.get().satisfiable
        return satisfiable

    def _get_minimum_uc(self, assumptions):

        powerset = chain.from_iterable(combinations(assumptions, r) for r in range(len(assumptions) + 1))

        for assumption_set in powerset:
            sat= self._solve_core(assumptions=assumption_set)
            if not sat:
                return assumption_set
        return []

    def _update_model(self):
        try:
            self._last_prg = ClinguinModel.get_cautious_brave(self._ctl,self._assumptions)
            self._model = ClinguinModel.from_widgets_file_and_program(self._ctl,self._widget_files,self._last_prg)

        except NoModelError as e:
            self._logger.info("UNSAT Answer, will add explanation")
            clingo_core = e.core
            clingo_core_symbols = [self._lit2symbol[s] for s in clingo_core]
            muc_core = self._get_minimum_uc(clingo_core_symbols)
            prg = self._last_prg
            for s in muc_core:
                prg = prg + f"_muc({str(s)})."
            self._model = ClinguinModel.from_widgets_file_and_program(self._ctl,self._widget_files,prg)



    
