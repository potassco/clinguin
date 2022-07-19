import clorm
import clingo


from clorm import Predicate, ConstantField, RawField, Raw
from clingo import Control
from clingo.symbol import Function, Number, String

from server.data.element import ElementDao
from server.data.attribute import AttributeDao
from server.data.callback import CallbackDao


class StandardClingoSolver:

    def __init__(self, logic_programs):
        
        self.ctl = Control()
        for f in logic_programs:
            self.ctl.load(str(f))
        self.ctl.ground([("base", [])])

        self.unifiers = [ElementDao, AttributeDao, CallbackDao]

    def getClingoWrapper(self, assumptions, brave_elements):
        wrapper = ClingoWrapper(self.ctl, self.unifiers, assumptions, brave_elements)
        wrapper.initCautiousFactbase()
        wrapper.initBraveFactbase()

        return wrapper


class ClingoWrapper:

    def __init__(self, ctl, unifiers, assumptions, brave_elements):
        self.ctl = ctl
        self.unifiers = unifiers
        self.assumptions = assumptions
        self.brave_elements = brave_elements

    def initCautiousFactbase(self):

        self.ctl.configuration.solve.enum_mode = 'cautious'
        self.ctl.solve(on_model=self._save_cautious, assumptions=[(clingo.parse_term(a),True) for a in list(self.assumptions)])

        factbase = clorm.unify(self.unifiers, self._cautious_model)

        self._cautious_factbase = factbase


    def initBraveFactbase(self):

        self.ctl.configuration.solve.enum_mode = 'brave'
        self.ctl.solve(on_model=self._save_brave, assumptions=[(clingo.parse_term(a),True) for a in list(self.assumptions)])

        factbase = clorm.unify(self.unifiers, self._brave_model)

        self._brave_factbase = factbase

    def getCautiousElements(self):
        return self._cautious_factbase.query(ElementDao).all()

    def getCautiousAttributesForElementId(self, element_id):
        return self._cautious_factbase.query(AttributeDao).where(AttributeDao.id == element_id).all()

    def getCautiousCallbacksForElementId(self, element_id):
        return self._cautious_factbase.query(CallbackDao).where(CallbackDao.id == element_id).all()

    def getBraveElements(self):
        brave_elements = []

 
        # TODO -> More efficient Query, where one queries for RawFields one selects only ''dropdownmenuitem''
        for t in self.brave_elements:
            for w in self._brave_factbase.query(ElementDao).all():
                if (str(w.type) == t):
                    brave_elements.append(w)

        return brave_elements

    def getBraveAttributesForElementId(self, element_id):
        return self._brave_factbase.query(AttributeDao).where(AttributeDao.id == element_id).all()

    def getBraveCallbacksForElementId(self, element_id):
        return self._brave_factbase.query(CallbackDao).where(CallbackDao.id == element_id).all()



    def _save_cautious(self, model):
        self._cautious_model = model.symbols(atoms=True, shown=True)

    def _save_brave(self, model):
        self._brave_model = model.symbols(atoms=True, shown=True)



