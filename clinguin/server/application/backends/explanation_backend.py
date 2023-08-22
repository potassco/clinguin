"""
Module that contains the Explanation Backend.
"""

import textwrap

from clingo.script import enable_python

from clinguin.server.application.backends.clingo_backend import ClingoBackend

enable_python()


class ExplanationBackend(ClingoBackend):
    """
    Backend for explanations
    """

    def __init__(self, args):
        self._muc = None
        self._lit2symbol = {}
        self._mc_base_assumptions = set()
        self._last_prg = None
        super().__init__(args)
        for a in args.assumption_signature:
            try:
                name = a.split(",")[0]
                arity = int(a.split(",")[1])
            except Exception:
                raise ValueError(
                    "Argument assumption_signature must have format name,arity"
                )
            for s in self._ctl.symbolic_atoms:
                if s.symbol.match(name, arity):
                    self._mc_base_assumptions.add(s.symbol)
                    self._add_symbol_to_dict(s.symbol)
        self._assumptions = self._mc_base_assumptions.copy()

    # ---------------------------------------------
    # Private methods
    # ---------------------------------------------

    def _add_symbol_to_dict(self, symbol):
        lit = self._ctl.symbolic_atoms[symbol].literal
        self._lit2symbol[lit] = symbol

    def _solve_core(self, assumptions):
        with self._ctl.solve(
            assumptions=[(a, True) for a in assumptions], yield_=True
        ) as solve_handle:
            satisfiable = solve_handle.get().satisfiable
            core = [self._lit2symbol[s] for s in solve_handle.core() if s != -1]
        return satisfiable, core

    def _get_minimum_uc(self, different_assumptions):
        sat, _ = self._solve_core(assumptions=different_assumptions)

        if sat:
            return []

        assumption_set = different_assumptions
        probe_set = []

        for i, assumption in enumerate(assumption_set):
            working_set = assumption_set[i + 1:]
            sat, _ = self._solve_core(assumptions=working_set + probe_set)
            if sat:
                probe_set.append(assumption)

                if not self._solve_core(assumptions=probe_set)[0]:
                    break

        return probe_set

    @property
    def _backend_state_prg(self):
        """
        Additional program to pass to the UI computation. It represents to the state of the backend
        """
        prg = super()._backend_state_prg
        if self._uifb.is_unsat:
            self._logger.info("UNSAT Answer, will add explanation")
            clingo_core = self._uifb._unsat_core
            clingo_core_symbols = [self._lit2symbol[s] for s in clingo_core if s != -1]
            muc_core = self._get_minimum_uc(clingo_core_symbols)
            for s in muc_core:
                prg = prg + f"_muc({str(s)})."
        return prg

    # ---------------------------------------------
    # Overwrite
    # ---------------------------------------------

    def _add_assumption(self, predicate_symbol):
        self._add_symbol_to_dict(predicate_symbol)
        self._assumptions.add(predicate_symbol)

    # ---------------------------------------------
    # Plolicy methods (Overwrite ClingoBackend)
    # ---------------------------------------------

    @classmethod
    def register_options(cls, parser):
        """
        Registers command line options for ClingraphBackend.
        """
        ClingoBackend.register_options(parser)

        parser.add_argument(
            "--assumption-signature",
            help=textwrap.dedent(
                """\
                            Signatures that will be considered as assumtions. Must be have format name,arity"""
            ),
            nargs="+",
            metavar="",
        )

    def clear_assumptions(self):
        self._end_browsing()
        self._assumptions = self._mc_base_assumptions.copy()
        self._update_uifb()
        return self.get()
