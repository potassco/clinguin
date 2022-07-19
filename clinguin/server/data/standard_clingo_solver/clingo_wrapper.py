import clorm
import clingo

from clinguin.server.data.element import ElementDao
from clinguin.server.data.attribute import AttributeDao
from clinguin.server.data.callback import CallbackDao

class ClingoWrapper:
    def __init__(self, instance, ctl, unifiers, assumptions, brave_elements):

        self._instance = instance
        self.ctl = ctl
        self.unifiers = unifiers
        self.assumptions = assumptions
        self.brave_elements = brave_elements

    def initFactbase(self):
        self.ctl.solve(on_model=self._save, assumptions=[(clingo.parse_term(a),True) for a in list(self.assumptions)])
        self._factbase = clorm.unify(self.unifiers, self._model)

    def getElements(self):
        return self._factbase.query(ElementDao).all()

    def getAttributesForElementId(self, element_id):
        return self._factbase.query(AttributeDao).where(AttributeDao.id == element_id).all()

    def getCallbacksForElementId(self, element_id):
        return self._factbase.query(CallbackDao).where(CallbackDao.id == element_id).all()

    def _save(self, model):
        self._model = model.symbols(atoms=True, shown=True)


