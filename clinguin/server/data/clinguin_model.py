from clorm import FactBasse

# TODO: All the Clorm unifier classes could go in this file here since they are so short and will be used only here (i think) (Sorry java)

from clinguin.server.data.element import ElementDao
from clinguin.server.data.attribute import AttributeDao
from clinguin.server.data.callback import CallbackDao

class ClinguinModel:

    def __init__(self, factbase=None):
        if factbase is None:
            self._factbase = FactBase([])
        else:
            self._factbase = factbase

    def getElements(self):
        return self._factbase.query(ElementDao).all()

    def getAttributesForElementId(self, element_id):
        return self._factbase.query(AttributeDao).where(AttributeDao.id == element_id).all()

    def getCallbacksForElementId(self, element_id):
        return self._factbase.query(CallbackDao).where(CallbackDao.id == element_id).all()

    def json(self):
        pass
        # Maybe we could have this here and remove of the standart json encoder class...
        # Or we keep the different class and call it ModelJsonEncoder
        # Just ideas


    def computeBrave(self, ctl, condition_on_symbols):
        pass
 
    def computeCautios(self, ctl, condition_on_symbols):
        pass
    
    def loadModel(self, m)
        pass