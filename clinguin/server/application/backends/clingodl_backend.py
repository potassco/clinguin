"""
Module that contains the ClingoDL Backend.
"""

from pathlib import Path

from clingo import Control
from clingo.ast import ProgramBuilder, parse_files
from clingo.script import enable_python
from clingodl import ClingoDLTheory

from clinguin.server.application.backends.clingo_multishot_backend import (
    ClingoMultishotBackend,
)

enable_python()
# pylint: disable=attribute-defined-outside-init


class ClingoDLBackend(ClingoMultishotBackend):
    """
    Backend that allows programs using clingodl theory atoms as input.
    It also includes the assignment in the domain state.
    """

    def __init__(self, args):
        super().__init__(args)

        # Model should be the last call so that the on_model takes the assignment of the model
        # and not of the cautious consequences
        self._domain_state_constructors.remove("_ds_model")
        self._add_domain_state_constructor("_ds_model")

        self._add_domain_state_constructor("_ds_assign")

    # ---------------------------------------------
    # Setups
    # ---------------------------------------------

    def _create_ctl(self):
        """
        Initializes the control object (domain-control).
        It is used when the server is started or after a restart.
        """
        super()._create_ctl()
        self._theory = ClingoDLTheory()
        self._theory.register(self._ctl)

    def _load_file(self, f):
        """
        Loads a file into the control. Uses the program builder to rewrite and add.

        Arguments:
            f (str): The file path
        """
        with ProgramBuilder(self._ctl) as bld:
            parse_files([f], lambda ast: self._theory.rewrite_ast(ast, bld.add))

    def _outdate(self):
        """
        Outdates all the dynamic values when a change has been made.
        Any current interaction in the models wil be terminated by canceling the search and removing the iterator.
        """
        super()._outdate()
        self._assignment = []

    # ---------------------------------------------
    # Solving
    # ---------------------------------------------

    def _prepare(self):
        # pylint: disable=attribute-defined-outside-init
        self._theory.prepare(self._ctl)

    def _on_model(self, model):
        self._theory.on_model(model)
        # pylint: disable=attribute-defined-outside-init
        self._assignment = list(
            (key, val) for key, val in self._theory.assignment(model.thread_id)
        )

    # ---------------------------------------------
    # Domain state
    # ---------------------------------------------

    @property
    def _ds_assign(self):
        """
        Additional program to pass to the UI computation with assignments
        """
        prg = ""
        for key, val in self._assignment:
            prg += f"_clinguin_assign({key},{val})."
        return prg
