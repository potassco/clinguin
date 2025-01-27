"""
Module that contains the ClingoDL Backend.
"""

import textwrap

from clingo.ast import ProgramBuilder, parse_files
from clingo.script import enable_python
from clingodl import ClingoDLTheory

from clinguin.server.application.backends.clingo_backend import (
    ClingoBackend,
)
from clinguin.utils.annotations import extends

enable_python()
# pylint: disable=attribute-defined-outside-init


class ClingoDLBackend(ClingoBackend):
    """
    Backend that allows programs using clingodl theory atoms as input.
    It also includes the assignment in the domain state.
    """

    # ---------------------------------------------
    # Setups
    # ---------------------------------------------

    @extends(ClingoBackend)
    def _init_command_line(self):
        """
        Sets the dl configuration
        """
        super()._init_command_line()
        dl_config = (
            [a.split("=") for a in self._args.dl_config] if self._args.dl_config else []
        )
        self._dl_conf = [(a[0], a[1]) for a in dl_config]

    @extends(ClingoBackend)
    def _init_interactive(self):
        """
        Initializes the list of the assignments

        Attributes:
            _assignment (List[Tuple[str, int]]): The list of assignments
        """
        super()._init_interactive()
        self._assignment = []

    @extends(ClingoBackend)
    def _init_ds_constructors(self):
        super()._init_ds_constructors()
        self._add_domain_state_constructor("_ds_assign")

    @extends(ClingoBackend)
    def _create_ctl(self):
        """
        Registers the ClingoDLTheory.
        """
        super()._create_ctl()
        self._theory = ClingoDLTheory()
        for k, v in self._dl_conf:
            self._theory.configure(k, v)
        self._theory.register(self._ctl)

    @extends(ClingoBackend)
    def _load_file(self, f):
        """
        Uses the program builder to rewrite the theory atoms.
        """
        with ProgramBuilder(self._ctl) as bld:
            parse_files([f], lambda ast: self._theory.rewrite_ast(ast, bld.add))

    @extends(ClingoBackend)
    def _outdate(self):
        """
        Sets the assignment to empty.
        """
        super()._outdate()
        self._assignment = []

    # ---------------------------------------------
    # Solving
    # ---------------------------------------------
    @extends(ClingoBackend)
    def _prepare(self):
        """
        Prepares the theory before solving
        """
        # pylint: disable=attribute-defined-outside-init
        self._theory.prepare(self._ctl)

    @extends(ClingoBackend)
    def _on_model(self, model):
        """
        Sets the assignment from the model
        """
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
    @extends(ClingoBackend)
    def register_options(cls, parser):
        """
        Adds the `dl-config` option.
        """
        ClingoBackend.register_options(parser)

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
        Adds program with assignments

        Includes predicate ``_clinguin_assign/2`` with the assignments.

        """
        if not self._ui_uses_predicate("_clinguin_assign", 2):
            return "% NOT USED\n"

        prg = ""
        for key, val in self._assignment:
            prg += f"_clinguin_assign({key},{val})."
        return prg
