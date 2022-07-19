from server.data.standard_clingo_solver.clingo_wrapper import ClingoWrapper

from server.data.element import ElementDao

class ClingoCautiousWrapper(ClingoWrapper): 

    def __init__(self, ctl, unifiers, assumptions, brave_elements):
        super().__init__(ctl, unifiers, assumptions, brave_elements)
        self.ctl.configuration.solve.enum_mode = 'cautious'

    def getElements(self):
        cautious_elements = []

        # TODO -> More efficient Query, where one queries for RawFields one selects only ''dropdownmenuitem''
        for w in self._factbase.query(ElementDao).all():
            for t in self.brave_elements:
                if (str(w.type) != t):
                    cautious_elements.append(w)

        return cautious_elements


