"""
Module that contains the ClinguinModel class.
"""
import logging
import clorm

from clorm import Raw
from clingo import Control,parse_term
from clingo.symbol import Function, Number, String

from clinguin.utils import NoModelError, Logger

from .element import ElementDao
from .attribute import AttributeDao
from .callback import CallbackDao

class ClinguinModel:
    """
    The ClinguinModel is the low-level-access-class for handling clorm and clingo, regarding brave-cautious and other default things. This class provides functionality to create a factbase with brave-cautious extended files, functionality to query important things for clinguin, etc.
    """

    def __init__(self, factbase=None):
        self._logger = logging.getLogger(Logger.server_logger_name)

        self.unifiers = [ElementDao, AttributeDao, CallbackDao]

        if factbase is None:
            self._factbase = clorm.FactBase([])
        else:
            self._factbase = factbase

    def __str__(self):
        return self._factbase.asp_str()

    @classmethod
    def from_widgets_file(cls, ctl, widgets_files, assumptions):
        """
        Creates a ClinguinModel from paths of widget files and assumptions.
        """
        prg = cls.get_cautious_brave(ctl,assumptions)
        return cls.from_widgets_file_and_program(ctl,widgets_files,prg)

    @classmethod
    def from_widgets_file_and_program(cls, ctl, widgets_files, prg):
        """
        Creates a ClinguinModel from a Clingo control object, paths of the widget-files and a logic program provided as a string (prg is a string which contains a logic program)
        """

        model = cls()

        wctl = cls.wid_control(widgets_files, prg)

        with wctl.solve(yield_=True) as result:
            for m in result:
                model_symbols = m.symbols(shown=True)
                break

        model._set_fb_symbols(model_symbols)
        return model

    @classmethod
    def wid_control(cls, widgets_files, extra_prg=""):
        """
        Generates a ClingoControl Object from paths of widget files and extra parts of a logic program given by a string.
        """
        wctl = Control(['0','--warn=none'])
        for f in widgets_files:
            try:
                wctl.load(str(f))
            except Exception as e:
                logger = logging.getLogger(Logger.server_logger_name)
                logger.critical("File %s  could not be loaded - likely not existant or syntax error in file!", str(f))
                raise e
        
        wctl.add("base",[],extra_prg)
        wctl.add("base",[],"#show element/3. #show attribute/3. #show callback/3.")
        wctl.ground([("base",[])])

        return wctl


    @classmethod
    def from_BC_extended_file(cls, ctl,assumptions):
        """
        Creates a ClinguinModel instance from a ClingoControl object and the provided assumptions.
        """

        logger = logging.getLogger(Logger.server_logger_name)

        ctl.assign_external(parse_term('show_all'),False)
        ctl.assign_external(parse_term('show_cautious'),False)
        ctl.assign_external(parse_term('show_untagged'),False)
        ctl.assign_external(parse_term('show_brave'),True)
        brave_model = cls.from_brave_model(ctl,assumptions, logger)
        # Here we could see if the user wants none tagged as cautious by default
        ctl.assign_external(parse_term('show_brave'),False)
        ctl.assign_external(parse_term('show_untagged'),True)
        cautious_model = cls.from_cautious_model(ctl,assumptions, logger)
        ctl.assign_external(parse_term('show_untagged'),False)
        ctl.assign_external(parse_term('show_all'),True)

        return cls.combine(brave_model,cautious_model, logger)
    

    @classmethod
    def combine(cls, cgmodel1, cgmodel2):
        """
        Combines the factbases of two ClinguinModels to one factbase, i.e. two ClinguinModels become one per Union.
        """
        return cls(cgmodel1._factbase.union(cgmodel2._factbase))

    @classmethod
    def from_clingo_model(cls, m):
        """ 
        Creates a ClinguinModel from a clingo model.
        """
        model = cls()
        model._set_fb_symbols(m.symbols(shown=True))
        return model

    @classmethod
    def from_brave_model(cls, ctl, assumptions):
        model = cls()
        brave_model = model.compute_brave(ctl, assumptions)
        model._set_fb_symbols(brave_model)
        return model

    @classmethod
    def from_cautious_model(cls, ctl, assumptions):
        model = cls()
        cautious_model = model.compute_cautious(ctl, assumptions)
        model._set_fb_symbols(cautious_model)
        return model

    @classmethod
    def get_cautious_brave(cls, ctl, assumptions):
        model = cls()

        cautious_model = model.compute_cautious(ctl, assumptions)
        brave_model = model.compute_brave(ctl, assumptions)
        # c_prg = self.tag_cautious_prg(cautious_model)
        c_prg = model.symbols_to_prg(cautious_model)
        b_prg = model.tag_brave_prg(brave_model)
        return c_prg+b_prg

    @classmethod
    def from_ctl(cls, ctl):
        model = cls()
        with ctl.solve(yield_=True) as result:
            for m in result:
                model_symbols = m.symbols(shown=True)
                break

        model._set_fb_symbols(model_symbols)
        return model


    def add_message(self,title,message):
        """
        Adds a ''Message'' (aka. Notification/Pop-Up) for the user with a certain title and message.
        """
        self.add_element("message","message","window")
        self.add_attribute("message","title",title)
        self.add_attribute("message","message",message)

    def tag(self, model, tag):
        tagged = []
        for s in model:
            tagged.append(Function(tag,[s]))
        return tagged

    def symbols_to_prg(self,symbols):
        return "\n".join([str(s)+"." for s in symbols])

    def tag_brave_prg(self, model):
        tagged = self.tag(model,'_b')
        return self.symbols_to_prg(tagged)
    
    def tag_cautious_prg(self, model):
        tagged = self.tag(model,'_c')
        return self.symbols_to_prg(tagged)


    def add_element(self, id, t, parent):
        if type(id)==str:
            id = Function(id,[])
        if type(t)==str:
            t = Function(t,[])
        if type(parent)==str:
            parent = Function(parent,[])
        self._factbase.add(ElementDao(Raw(id),Raw(t),Raw(parent)))

    def add_attribute(self, id, key, value):
        if type(id)==str:
            id = Function(id,[])
        if type(key)==str:
            key = Function(key,[])
        if type(value)==str:
            value = String(value)
        if type(value)==int:
            value = Number(value)
        self._factbase.add(AttributeDao(Raw(id),Raw(key),Raw(value)))

    def filter_elements(self, condition):
        elements = self.get_elements()
        kept_elements = [e for e in elements if condition(e)]
        kept_ids = [e.id for e in kept_elements]
        attributes = self.get_attributes()
        callbacks = self.get_callbacks()
        kept_attributes = [e for e in attributes if e.id in kept_ids]
        kept_callbacks = [e for e in callbacks if e.id in kept_ids]
        self._factbase=clorm.FactBase(kept_elements+kept_callbacks+kept_attributes)

    def get_elements(self):
        return self._factbase.query(ElementDao).all()
    
    def get_attributes(self):
        return self._factbase.query(AttributeDao).all()

    def get_attributesGrouped(self):
        return self._factbase.query(AttributeDao).group_by(AttributeDao.id).all()

    def get_callbacksGrouped(self):
        return self._factbase.query(CallbackDao).group_by(CallbackDao.id).all()

    def get_callbacks(self):
        return self._factbase.query(CallbackDao).all()

    def get_attributesForElementId(self, element_id):
        return self._factbase.query(AttributeDao).where(
            AttributeDao.id == element_id).all()

    def get_callbacksForElementId(self, element_id):
        return self._factbase.query(CallbackDao).where(
            CallbackDao.id == element_id).all()
    
    def _set_fb_symbols(self, symbols):
        self._factbase = clorm.unify(self.unifiers, symbols)

    def _compute(self,ctl, assumptions):
        with ctl.solve(assumptions=[(a,True) for a in assumptions],
                yield_=True) as result:
            model_symbols = None
            for m in result:
                model_symbols = m.symbols(shown=True,atoms=False)
        if model_symbols is None:
            raise NoModelError
        return list(model_symbols)

    def compute_brave(self, ctl, assumptions):
        ctl.configuration.solve.enum_mode = 'brave'
        return self._compute(ctl, assumptions)
    
    def compute_cautious(self, ctl, assumptions):
        ctl.configuration.solve.enum_mode = 'cautious'
        return self._compute(ctl, assumptions)

    def compute_auto(self, ctl, assumptions):
        ctl.configuration.solve.enum_mode = 'auto'
        return self._compute(ctl, assumptions)


    def get_factbase(self):
        return self._factbase

