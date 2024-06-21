"""
Module that contains the ClingoDL Backend.
"""

from pathlib import Path
import textwrap

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
        dl_config = [a.split("=") for a in args.dl_config] if args.dl_config else []
        self._dl_conf = [(a[0], a[1]) for a in dl_config]

        super().__init__(args)

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
        for k, v in self._dl_conf:
            self._theory.configure(k, v)
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
        super()._on_model(model)
        self._theory.on_model(model)
        # pylint: disable=attribute-defined-outside-init
        self._assignment = list(
            (key, val) for key, val in self._theory.assignment(model.thread_id)
        )

    # ---------------------------------------------
    # Class methods
    # ---------------------------------------------

    @classmethod
    def register_options(cls, parser):
        """
        Registers command line options.
        """
        ClingoMultishotBackend.register_options(parser)

        parser.add_argument(
            "--dl-config",
            help=textwrap.dedent(
                """\
                    Clingo-dl options list of <parameter>=<value>.
                 """
            ),
            nargs="*",
        )

    # ---------------------------------------------
    # Domain state
    # ---------------------------------------------

    @property
    def _ds_assign(self):
        """
        Additional program to pass to the UI computation with assignments
        """
        if not self._ui_uses_predicate("_clinguin_assign", 2):
            return ""
        prg = ""
        for key, val in self._assignment:
            prg += f"_clinguin_assign({key},{val})."
        return prg
