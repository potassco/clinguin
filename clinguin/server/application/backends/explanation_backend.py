"""
Module that contains the Explanation Backend.
"""

import textwrap
from functools import cached_property

from clingo.script import enable_python
from clingexplaid.transformers import AssumptionTransformer
from clingexplaid.mus import CoreComputer


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
        self._mus = None
        self._mc_base_assumptions = set()
        self._parse_assumption_signature(args)
        self._assumption_transformer = AssumptionTransformer(
            signatures=self._assumption_sig
        )
        super().__init__(args)
        self._transformer_assumptions = self._assumption_transformer.get_assumptions(
            self._ctl, symbols=True
        )

        self._add_domain_state_constructor("_ds_mus")

    # ---------------------------------------------
    # Private methods
    # ---------------------------------------------

    def _parse_assumption_signature(self, args):
        """
        Parse assumption signatures in the arguments
        """
        self._assumption_sig = []
        for a in args.assumption_signature:
            try:
                self._assumption_sig.append((a.split(",")[0], int(a.split(",")[1])))
            except Exception as ex:
                raise ValueError(
                    "Argument assumption_signature must have format name,arity"
                ) from ex

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
                            Signatures that will be considered as true assumptions. Must be have format name,arity"""
            ),
            nargs="+",
            metavar="",
        )

    # ---------------------------------------------
    # Setups
    # ---------------------------------------------

    def _load_file(self, f):
        """
        Loads a file into the control. Transforms the program to add choices around assumption signatures.

        Arguments:
            f (str): The file path
        """

        transformed_program = self._assumption_transformer.parse_files([f])
        self._ctl.add("base", [], transformed_program)

    def _get_assumptions(self):
        """
        Gets the set of assumptions used for solving
        """

        return self._assumptions.union(self._transformer_assumptions)

    def _outdate(self):
        """
        Outdates all the dynamic values when a change has been made.
        Any current interaction in the models wil be terminated by canceling the search and removing the iterator.
        """
        super()._outdate()
        self._clear_cache(["_ds_mus"])

    # ---------------------------------------------
    # Domain state
    # ---------------------------------------------

    @cached_property
    def _ds_mus(self):
        """
        Adds information about the Minimal Unsatisfiable Set (MUS)
        Includes predicate ``_clinguin_mus/1`` for every assumption in the MUC
        It uses a cache that is erased after an operation makes changes in the control.
        """
        prg = "#defined _clinguin_mus/1.\n"
        if self._unsat_core is not None:
            self._logger.info("UNSAT Answer, will add explanation")
            cc = CoreComputer(self._ctl, [(a, True) for a in self._get_assumptions()])
            cc.shrink()
            mus_core = cc.minimal
            for s, v in mus_core:
                prg = prg + f"_clinguin_mus({str(s)}).\n"
        return prg
