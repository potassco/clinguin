from clinguin.server.data.standard_clingo_solver.clingo_wrapper import ClingoWrapper

from clinguin.server.data.element import ElementDao

class ClingoBraveWrapper(ClingoWrapper):
    
    def __init__(self, instance, ctl, unifiers, assumptions, brave_elements):
        super().__init__(instance, ctl, unifiers, assumptions, brave_elements)
        self.ctl.configuration.solve.enum_mode = 'brave'

    def getElements(self):
        brave_elements = []
 
        # TODO -> More efficient Query, where one queries for RawFields one selects only ''dropdownmenuitem''
        for t in self.brave_elements:
            for w in self._factbase.query(ElementDao).all():
                if (str(w.type) == t):
                    brave_elements.append(w)

        return brave_elements



