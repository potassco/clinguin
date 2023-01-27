"""
Module that contains the Explanation Backend.
"""

from functools import partial
from re import A
from clingo import parse_term
from clingo.script import enable_python

from clinguin.server import ClinguinModel
from clinguin.server.application.backends.clingo_backend import ClingoBackend
from clinguin.server.application.backends.standard_utils.brave_cautious_helper import *
from clinguin.utils import NoModelError

enable_python()


class ExplanationBackend(ClingoBackend):
    """
    Backend for explanations
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
    
    # ---------------------------------------------
    # Private methods
    # ---------------------------------------------

    def _add_symbol_to_dict(self,symbol):
        lit = self._ctl.symbolic_atoms[symbol].literal
        self._lit2symbol[lit]=symbol


    def _solve_core(self, assumptions):
        with self._ctl.solve(assumptions=[(a,True) for a in assumptions], yield_=True) as solve_handle:
            satisfiable = solve_handle.get().satisfiable
            core = [self._lit2symbol[index] for index in solve_handle.core()]
        return satisfiable, core

    def _get_minimum_uc(self, different_assumptions):
        sat, _ = self._solve_core(assumptions=different_assumptions)

        if sat:
            return []

        assumption_set = different_assumptions
        probe_set = []

        for i, assumption in enumerate(assumption_set):
            working_set = assumption_set[i+1:]
            sat, _ = self._solve_core(assumptions=working_set + probe_set)
            if sat:
                probe_set.append(assumption)

                if not self._solve_core(assumptions=probe_set)[0]:
                    break

        return probe_set


    # ---------------------------------------------
    # Overwrite
    # ---------------------------------------------

    def _update_model(self):
        try:
            self._last_prg = ClinguinModel.get_cautious_brave(self._ctl,self._assumptions)
            self._model = ClinguinModel.from_ui_file_and_program(self._ctl,self._ui_files,self._last_prg,self._assumptions)

        except NoModelError as e:
            self._logger.info("UNSAT Answer, will add explanation")
            clingo_core = e.core
            clingo_core_symbols = [self._lit2symbol[s] for s in clingo_core]
            muc_core = self._get_minimum_uc(clingo_core_symbols)
            prg = self._last_prg
            for s in muc_core:
                prg = prg + f"_muc({str(s)})."
            self._model = ClinguinModel.from_ui_file_and_program(self._ctl,self._ui_files,prg,self._assumptions)

    

    # ---------------------------------------------
    # Plolicy methods (Overwrite ClingoBackend)
    # ---------------------------------------------

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
