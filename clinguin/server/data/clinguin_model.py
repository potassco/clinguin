import clorm
import clingo
import logging

from clorm import Predicate, ConstantField, RawField, Raw
from clingo import Control,parse_term
from clingo.symbol import Function, Number, String

from clinguin.server.data.element import ElementDao
from clinguin.server.data.attribute import AttributeDao
from clinguin.server.data.callback import CallbackDao


class ClinguinModel:

    def __init__(self, factbase=None):

        self.unifiers = [ElementDao, AttributeDao, CallbackDao]

        if factbase is None:
            self._factbase = clorm.FactBase([])
        else:
            self._factbase = factbase

    def __str__(self):
        return self._factbase.asp_str()

    # @classmethod
    # def fromBraveTaggedFile(cls, ctl, assumptions):
    #     model = cls()
    #     brave_model = model.computeBrave(ctl, assumptions)
    #     brave_symbols = [b.arguments[0] for b in brave_model if b.match('_brave',1)]
    #     cautious_symbols = model.computeCautious(ctl, assumptions)
    #     print(cautious_symbols)
    #     model._setFbSymbols(brave_symbols + cautious_symbols)
    #     return model

    @classmethod
    def fromBCExtendedFile(cls, ctl,assumptions):
        model = cls()
        ctl.assign_external(parse_term('show_untagged'),False)
        ctl.assign_external(parse_term('show_cautious'),False)
        ctl.assign_external(parse_term('show_brave'),True)
        brave_model = cls.fromBraveModel(ctl,assumptions)
        # Here we could see if the user wants none tagged as cautious by default
        ctl.assign_external(parse_term('show_brave'),False)
        ctl.assign_external(parse_term('show_untagged'),True)
        cautious_model = cls.fromCautiousModel(ctl,assumptions)
        return cls.combine(brave_model,cautious_model)
    

    @classmethod
    def combine(cls, cgmodel1, cgmodel2):
        return cls(cgmodel1._factbase.union(cgmodel2._factbase))


    @classmethod
    def fromBraveModel(cls, ctl, assumptions):
        model = cls()
        brave_model = model.computeBrave(ctl, assumptions)
        model._setFbSymbols(brave_model)
        return model

    @classmethod
    def fromCautiousModel(cls, ctl, assumptions):
        model = cls()
        cautious_model = model.computeCautious(ctl, assumptions)
        model._setFbSymbols(cautious_model)
        return model

    def filterElements(self, condition):
        elements = self.getElements()
        kept_elements = [e for e in elements if condition(e)]
        kept_ids = [e.id for e in kept_elements]
        attributes = self.getAttributes()
        callbacks = self.getCallbacks()
        kept_attributes = [e for e in attributes if e.id in kept_ids]
        kept_callbacks = [e for e in callbacks if e.id in kept_ids]
        self._factbase=clorm.FactBase(kept_elements+kept_callbacks+kept_attributes)

    def getElements(self):
        return self._factbase.query(ElementDao).all()
    
    def getAttributes(self):
        return self._factbase.query(AttributeDao).all()

    def getAttributesGrouped(self):
        return self._factbase.query(AttributeDao).group_by(AttributeDao.id).all()

    def getCallbacksGrouped(self):
        return self._factbase.query(CallbackDao).group_by(CallbackDao.id).all()

    def getCallbacks(self):
        return self._factbase.query(CallbackDao).all()

    def getAttributesForElementId(self, element_id):
        return self._factbase.query(AttributeDao).where(
            AttributeDao.id == element_id).all()

    def getCallbacksForElementId(self, element_id):
        return self._factbase.query(CallbackDao).where(
            CallbackDao.id == element_id).all()
    
    def _setFbSymbols(self, symbols):
        self._factbase = clorm.unify(self.unifiers, symbols)

    def _compute(self,ctl, assumptions):
        symbols = []
        with ctl.solve(assumptions=[(parse_term(a),True) for a in assumptions],
                yield_=True) as result:
            model_symbols = None
            for m in result:
                model_symbols = m.symbols(shown=True,atoms=False)
        return list(model_symbols)

    def computeBrave(self, ctl, assumptions):
        ctl.configuration.solve.enum_mode = 'brave'
        return self._compute(ctl, assumptions)
    
    def computeCautious(self, ctl, assumptions):
        ctl.configuration.solve.enum_mode = 'cautious'
        return self._compute(ctl, assumptions)

    def computeAuto(self, ctl, assumptions):
        ctl.configuration.solve.enum_mode = 'auto'
        return self._compute(ctl, assumptions)



