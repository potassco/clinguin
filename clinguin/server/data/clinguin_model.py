import clorm
import clingo
import logging

from clorm import Predicate, ConstantField, RawField, Raw
from clingo import Control
from clingo.symbol import Function, Number, String

from clinguin.server.data.element import ElementDao
from clinguin.server.data.attribute import AttributeDao
from clinguin.server.data.callback import CallbackDao

class ClinguinModel:

    def __init__(self, files, logger, factbase=None):

        self._logger = logger
        self.unifiers = [ElementDao, AttributeDao, CallbackDao]

        if factbase is None:
            self._factbase = clorm.FactBase([])
        else:
            self._factbase = factbase

    def getElements(self):
        return self._factbase.query(ElementDao).all()

    def getAttributesForElementId(self, element_id):
        return self._factbase.query(AttributeDao).where(AttributeDao.id == element_id).all()

    def getCallbacksForElementId(self, element_id):
        return self._factbase.query(CallbackDao).where(CallbackDao.id == element_id).all()

    def computeBrave(self, ctl, assumptions, condition_on_symbols):
        ctl.configuration.solve.enum_mode = 'brave'
        self._compute(ctl, assumptions, condition_on_symbols)

    def computeCautious(self, ctl, assumptions, condition_on_symbols):
        ctl.configuration.solve.enum_mode = 'cautious'
        self._compute(ctl, assumptions, condition_on_symbols)

    def _compute(self, ctl, assumptions, condition_on_symbols):
        ctl.solve(on_model=self._save, assumptions=[(clingo.parse_term(a),True) for a in list(assumptions)])
        if self._model:
            tmp_factbase = clorm.unify(self.unifiers, self._model)

            for w in tmp_factbase.query(ElementDao).all():
                if (condition_on_symbols(w)):
                    self._factbase.add(w)
                    for attr in tmp_factbase.query(AttributeDao).all():
                        if str(attr.id) == str(w.id):
                            self._factbase.add(attr)

                    for call in tmp_factbase.query(CallbackDao).all():
                        if str(call.id) == str(w.id):
                            self._factbase.add(call)
    def _save(self, model):
        self._model = model.symbols(atoms=True, shown=True)


