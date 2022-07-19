import clorm
import clingo


from clorm import Predicate, ConstantField, RawField, Raw
from clingo import Control
from clingo.symbol import Function, Number, String

from clinguin.server.data.element import ElementDao
from clinguin.server.data.attribute import AttributeDao
from clinguin.server.data.callback import CallbackDao

from clinguin.server.data.standard_clingo_solver.clingo_cautious_wrapper import ClingoCautiousWrapper
from clinguin.server.data.standard_clingo_solver.clingo_brave_wrapper import ClingoBraveWrapper
from clinguin.server.data.standard_clingo_solver.data_wrapper import DataWrapper


class StandardClingoSolver:

    def __init__(self, logic_programs, instance):
        self._instance = instance
        
        self.ctl = Control()
        for f in logic_programs:
            self.ctl.load(str(f))
        self.ctl.ground([("base", [])])

        self.unifiers = [ElementDao, AttributeDao, CallbackDao]

    def getClingoWrapper(self, assumptions, brave_elements):
        cautious_wrapper = ClingoCautiousWrapper(self._instance, self.ctl, self.unifiers, assumptions, brave_elements)
        cautious_wrapper.initFactbase()
        brave_wrapper = ClingoBraveWrapper(self._instance, self.ctl, self.unifiers, assumptions, brave_elements)
        brave_wrapper.initFactbase()


        wrapper = DataWrapper(cautious_wrapper, brave_wrapper)
        return wrapper

