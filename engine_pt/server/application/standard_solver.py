import networkx as nx
from typing import Sequence, Any

from server.application.standard_json_encoder import StandardJsonEncoder
from server.data.standard_clingo_solver.standard_clingo_solver import StandardClingoSolver
class StandardSolver:

    def __init__(self, logic_programs):

        self._clingo_solver = StandardClingoSolver(logic_programs)
        self._json_encoder = StandardJsonEncoder()

        self.assumptions = set()
        self.assumptions_map = {}
        self.brave_elements = ['dropdownmenuitem']

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

        wrapper = self._clingo_solver.getClingoWrapper(self.assumptions, self.brave_elements)
        class_hierarchy = self._json_encoder.encode(wrapper)

        # Automatic serialization happens here
        return class_hierarchy


