import clorm
import clingo


from clorm import Predicate, ConstantField, RawField, Raw
from clingo import Control
from clingo.symbol import Function, Number, String

from server.data.element import ElementDao
from server.data.attribute import AttributeDao
from server.data.callback import CallbackDao

from server.data.standard_clingo_solver.clingo_cautious_wrapper import ClingoCautiousWrapper
from server.data.standard_clingo_solver.clingo_brave_wrapper import ClingoBraveWrapper
from server.data.standard_clingo_solver.data_wrapper import DataWrapper


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

