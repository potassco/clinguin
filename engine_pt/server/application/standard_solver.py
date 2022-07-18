import clingo
import clorm
import networkx as nx

from clorm import Predicate, ConstantField, RawField, Raw
from clingo import Control
from clingo.symbol import Function, Number, String

from typing import Sequence, Any

from server.data.element import ElementDao
from server.data.attribute import AttributeDao
from server.data.callback import CallbackDao

from server.application.standard_json_encoder import StandardJsonEncoder

class StandardSolver:

    def __init__(self, logic_programs):

        self.assumptions = set()
        self.assumptions_map = {}
        
        self.ctl = Control()
        for f in logic_programs:
            self.ctl.load(str(f))
        self.ctl.ground([("base", [])])

        self.unifiers = [ElementDao, AttributeDao, CallbackDao]

    def assume(self, predicate) -> bool:
        if predicate not in self.assumptions:
            self.assumptions.add(predicate)
            return True
        else:
            return False


    def remove(self, predicate) -> bool:
        if predicate in self.assumptions:
            self.assumptions.remove(predicate)
            self.assumptions.remove("assume(" + predicate + ")")
            return True
        else:
            return False

    def solve(self) -> Any:
        print('SOLVE()')

        self.ctl.configuration.solve.enum_mode = 'cautious'
        self.ctl.solve(on_model=self._save_cautious, assumptions=[(clingo.parse_term(a),True) for a in list(self.assumptions)])
        prg = "\n".join([str(s) + "." for s in self._cautious_model])

        encoder = StandardJsonEncoder(prg)
        classHierarchy = encoder.solve()

        self.ctl.configuration.solve.enum_mode = 'brave'
        self.ctl.solve(on_model=self._save_brave, assumptions=[(clingo.parse_term(a),True) for a in list(self.assumptions)])
        prg = "\n".join([str(s) + "." for s in self._brave_model])

        classHierarchy = encoder.addBraveElements(classHierarchy, prg, ['dropdownmenuitem'])


        # Automatic serialization happens here
        return classHierarchy

    def _save_cautious(self, model):
        self._cautious_model = model.symbols(atoms=True, shown=True)

    def _save_brave(self, model):
        self._brave_model = model.symbols(atoms=True, shown=True)



