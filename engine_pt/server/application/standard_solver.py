import clingo
import clorm
import networkx as nx

from clorm import Predicate, ConstantField, RawField, Raw
from clingo import Control
from clingo.symbol import Function, Number, String

from server.data.element import ElementDao
from server.data.attribute import AttributeDao
from server.data.callback import CallbackDao

from server.application.standard_json_encoder import StandardJsonEncoder

class StandardSolver:

    def __init__(self, logic_programs):
        print(logic_programs)
        
        self.ctl = Control()
        for f in logic_programs:
            self.ctl.load(str(f))
        self.ctl.ground([("base", [])])

        self.unifiers = [ElementDao, AttributeDao, CallbackDao]

    def assume(self, test):
        print('<<-ENGINE-1: ' + test + ' >>')
        return '<<-ENGINE-1: ' + test + ' >>'

    def solve(self):
        print('SOLVE()')

        self.ctl.configuration.solve.enum_mode = 'cautious'
        self.ctl.solve(on_model=self._save_cautious)
        prg = "\n".join([str(s) + "." for s in self._cautious_model])

        encoder = StandardJsonEncoder(prg)
        classHierarchy = encoder.solve()
        # Automatic serialization happens here
        return classHierarchy

    def _save_cautious(self, model):
        self._cautious_model = model.symbols(atoms=True, shown=True)


