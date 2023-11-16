"""
Module that contains the ClingoDL Backend.
"""

import textwrap

from clingo.script import enable_python
from pathlib import Path

from clinguin.server.application.backends.clingo_multishot_backend import ClingoMultishotBackend
from clingodl import ClingoDLTheory
from clingo import Control
from clingo.ast import ProgramBuilder, parse_files

enable_python()


class ClingoDLBackend(ClingoMultishotBackend):
    """
    Backend for explanations
    """

    def __init__(self, args):
        super().__init__(args)
        

    # ---------------------------------------------
    # Private methods
    # ---------------------------------------------


    # ---------------------------------------------
    # Overwrite
    # ---------------------------------------------

    def _init_ctl(self):
        self._ctl = Control(["0"] + self._constants)
        self._theory = ClingoDLTheory()
        self._theory.register(self._ctl)

        existant_file_counter = 0
        with ProgramBuilder(self._ctl) as bld:
            
            for f in self._domain_files:
                path = Path(f)
                if path.is_file():
                    try:
                        parse_files([f], lambda ast: self._theory.rewrite_ast(ast, bld.add))
                        existant_file_counter += 1
                    except Exception:
                        self._logger.critical(
                            "Failed to load file %s (there is likely a syntax error in this logic program file).",f,)
                else:
                    self._logger.critical(
                        "File %s does not exist, this file is skipped.", f)

        if existant_file_counter == 0:
            exception_string = (
                "None of the provided domain files exists or they can't be parsed by clingo. At least one syntactically"
                + "valid domain file must be specified."
            )
            raise Exception(exception_string)

        for atom in self._atoms:
            self._ctl.add("base", [], str(atom) + ".")

    def _solve_set_handler(self):
        self._theory.prepare(self._ctl)
        self._handler = self._ctl.solve(
                assumptions=[(a, True) for a in self._assumptions], yield_=True
            )
    

    def _on_model(self, model):
        self._theory.on_model(model)
        self._assignment = [f'_clinguin_assign({key},{val}).' for key, val in self._theory.assignment(model.thread_id)]

    @property
    def _clinguin_state(self):
        """
        Additional program to pass to the UI computation. It represents to the state of the backend
        """
        prg = super()._clinguin_state
        prg += " ".join(self._assignment)
        return prg
    
    # ---------------------------------------------
    # Plolicy methods (Overwrite ClingoMultishotBackend)
    # ---------------------------------------------

