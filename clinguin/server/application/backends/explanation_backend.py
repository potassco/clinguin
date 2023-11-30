"""
Module that contains the Explanation Backend.
"""

import textwrap
from functools import cached_property

from clingo.script import enable_python

from clinguin.server.application.backends.clingo_multishot_backend import (
    ClingoMultishotBackend,
)

enable_python()


class ExplanationBackend(ClingoMultishotBackend):
    """
    Extends ClingoMultishotBackend. This backend will treat an UNSAT result by adding the
    Minimal Unsatisfiable Core (MUC) to the domain-state, thus allowing the UI to show
    the faulty assumptions.
    """

    def __init__(self, args):
        self._muc = None
        self._lit2symbol = {}
        self._mc_base_assumptions = set()
        super().__init__(args)

        self._add_domain_state_constructor("_ds_muc")

        for a in args.assumption_signature:
            try:
                name = a.split(",")[0]
                arity = int(a.split(",")[1])
            except Exception as ex:
                raise ValueError(
                    "Argument assumption_signature must have format name,arity"
                ) from ex
            for s in self._ctl.symbolic_atoms:
                if s.symbol.match(name, arity):
                    self._mc_base_assumptions.add(s.symbol)
                    self._add_symbol_to_dict(s.symbol)
        self._assumptions = self._mc_base_assumptions.copy()

    # ---------------------------------------------
    # Class methods
    # ---------------------------------------------

    @classmethod
    def register_options(cls, parser):
        """
        Registers command line options for ClingraphBackend.
        """
        ClingoMultishotBackend.register_options(parser)

        parser.add_argument(
            "--assumption-signature",
            help=textwrap.dedent(
                """\
                            Signatures that will be considered as assumtions. Must be have format name,arity"""
            ),
            nargs="+",
            metavar="",
        )

    # ---------------------------------------------
    # Setups
    # ---------------------------------------------

    def _outdate(self):
        """
        Outdates all the dynamic values when a change has been made.
        Any current interaction in the models wil be terminated by canceling the search and removing the iterator.
        """
        super()._outdate()
        self._clear_cache(["_ds_muc"])

    # ---------------------------------------------
    # Solving
    # ---------------------------------------------

    def _add_assumption(self, predicate_symbol):
        """
        Adds an assumption by also including in the mapping to literals.
        """
        super()._add_assumption(predicate_symbol)
        self._add_symbol_to_dict(predicate_symbol)

    # ---------------------------------------------
    # Domain state
    # ---------------------------------------------

    @cached_property
    def _ds_muc(self):
        """
        Adds information about the Minimal Unsat Core (MUC)
        Includes predicate ``_clinguin_muc/1`` for every assumption in the MUC
        It uses a cache that is erased after an operation makes changes in the control.
        """
        prg = "#defined _clinguin_muc/1."
        if self._unsat_core is not None:
            self._logger.info("UNSAT Answer, will add explanation")
            clingo_core = self._unsat_core
            clingo_core_symbols = [self._lit2symbol[s] for s in clingo_core if s != -1]
            muc_core = self._get_minimum_uc(clingo_core_symbols)
            for s in muc_core:
                prg = prg + f"_clinguin_muc({str(s)})."
        return prg

    # ---------------------------------------------
    # Private methods
    # ---------------------------------------------

    def _add_symbol_to_dict(self, symbol):
        """
        Adds a list of symbols to the mapping of symbols to literals
        """
        lit = self._ctl.symbolic_atoms[symbol].literal
        self._lit2symbol[lit] = symbol

    def _solve_core(self, assumptions):
        """
        Solves and gets the core with the basic faulty assumptions.

        Arguments:

            assumptions (list[int]): List of assumption literals
        """
        with self._ctl.solve(
            assumptions=[(a, True) for a in assumptions], yield_=True
        ) as solve_handle:
            satisfiable = solve_handle.get().satisfiable
            core = [self._lit2symbol[s] for s in solve_handle.core() if s != -1]
        return satisfiable, core

    def _get_minimum_uc(self, different_assumptions):
        """
        Computes the MUC from the assumptions

        Arguments:

            different_assumptions (list[int]): List of assumption literals that is being minimized
        """
        sat, _ = self._solve_core(assumptions=different_assumptions)

        if sat:
            return []

        assumption_set = different_assumptions
        probe_set = []

        for i, assumption in enumerate(assumption_set):
            working_set = assumption_set[i + 1 :]
            sat, _ = self._solve_core(assumptions=working_set + probe_set)
            if sat:
                probe_set.append(assumption)

                if not self._solve_core(assumptions=probe_set)[0]:
                    break

        return probe_set

    ########################################################################################################

    # ---------------------------------------------
    # Public operations
    # ---------------------------------------------

    def clear_assumptions(self):
        """
        Removes all assumptions. Overwrites the parent method by keeping as assumptions
        the ones provided as input via the command line.
        """
        self._outdate()
        self._assumptions = self._mc_base_assumptions.copy()
