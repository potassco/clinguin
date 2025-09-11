"""
Module that contains the Clingcon Backend.
"""

from clingo.ast import Location, Position, ProgramBuilder, Rule, parse_files
from clingcon import ClingconTheory
from fclingo import THEORY, Translator
from fclingo.__main__ import DEF, Statistic
from fclingo.parsing import HeadBodyTransformer

from clinguin.server.application.backends.theory_backend import TheoryBackend
from clinguin.utils.annotations import extends


class Config:
    def __init__(self, max_int, min_int, print_trans, defined) -> None:
        self.max_int = max_int
        self.min_int = min_int
        self.print_trans = print_trans
        self.defined = defined


class F(TheoryBackend):
    """
    Backend that allows programs using fclingo theory atoms as input.
    It also includes the assignment in the domain state.
    """

    theory_class = ClingconTheory

    @extends(TheoryBackend)
    def _load_file(self, f):
        """
        Uses the program builder to rewrite the theory atoms.
        """
        with ProgramBuilder(self._ctl) as bld:
            hbt = HeadBodyTransformer()
            parse_files([f], lambda ast: bld.add(hbt.visit(ast)))
            pos = Position("<string>", 1, 1)
            loc = Location(pos, pos)
            for rule in hbt.rules_to_add:
                bld.add(Rule(loc, rule[0], rule[1]))

    @extends(TheoryBackend)
    def _ground(self, program="base", arguments=None):
        super()._ground(program, arguments)
        max_int = next((x[1] for x in self._theory_conf if x[0] == "max-int"), 1000)
        min_int = next((x[1] for x in self._theory_conf if x[0] == "min-int"), -1000)
        translator = Translator(
            self._ctl, Config(max_int, min_int, False, DEF), Statistic()
        )
        translator.translate(self._ctl.theory_atoms)

    @extends(TheoryBackend)
    def _create_ctl(self):
        """
        Registers the ClingconTheory.
        """
        super()._create_ctl()
        self._ctl.add("base", [], THEORY)
