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

        self._add_domain_state_constructor("_ds_assign")

    # ---------------------------------------------
    # Setups
    # ---------------------------------------------

    def _init_ctl(self):
        self._ctl = Control(["0"] + self._constants)
        self._theory = ClingoDLTheory()
        self._theory.register(self._ctl)

        with ProgramBuilder(self._ctl) as bld:
            for f in self._domain_files:
                path = Path(f)
                if not path.is_file():
                    self._logger.critical("File %s does not exist", f)
                    raise Exception(f"File {f} does not exist")
                try:
                    parse_files([f], lambda ast: self._theory.rewrite_ast(ast, bld.add))
                except Exception as a:
                    self._logger.critical(
                        "Failed to load file %s (there is likely a syntax error in this logic program file).",
                        f,
                    )
                    raise a

        for atom in self._atoms:
            self._ctl.add("base", [], str(atom) + ".")

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
            (key, val) for key, val in self._theory.assignment(model.thread_id))

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
