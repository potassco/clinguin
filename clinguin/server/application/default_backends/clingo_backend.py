from clinguin.utils.errors import NoModelError
import networkx as nx
import sys
from typing import Sequence, Any

import logging
import clingo
from clingo import Control, parse_term
from clingo.script import enable_python
enable_python()
from clingo.symbol import Function, Number, String

# Self defined
from clinguin.server import StandardJsonEncoder

from clinguin.server import ClinguinModel

from clinguin.server import ClinguinBackend

from clinguin.server.application.default_backends.standard_utils.brave_cautious_helper import *

class ClingoBackend(ClinguinBackend):

    def __init__(self, args):
        super().__init__(args)
        self._souce_files = args.source_files
        self._widget_files = args.widget_files
        
        # For browising
        self._handler=None
        self._iterator=None
        
        self._restart()
        
        # I think we should remove this and only have one ClinguinModel
        self._modelClass = ClinguinModel
        self._model=None
        self._updateModel()




    @classmethod
    def registerOptions(cls, parser):
        parser.add_argument('source_files', nargs='+', help='Files')
        parser.add_argument('widget_files', nargs='+', help='Files')


    def _restart(self):
        self._endBrowsing()
        self._assumptions = set()
        self._atoms = set()
        self._initCtl()
        self._ground()

    def _initCtl(self):
        self._ctl = Control(['0'])
        for f in self._souce_files:
            try:
                self._ctl.load(str(f))
            except Exception as e:
                self._logger.fatal(str(e))
                self._logger.fatal("Failed to load modules (there is likely a syntax error in your logic program), now exiting - see previous stack trace for more information.")
                sys.exit()
        
        for atom in self._atoms:
            self._ctl.add("base",[],str(atom) + ".")
        
        
        # Only if an option is active
        # self._ctl.add("base",[],brave_cautious_externals)
    
    def _ground(self):
        self._ctl.ground([("base", [])])

        # Only if an option is active
        # self._ctl.assign_external(parse_term('show_all'),True
    
    def _endBrowsing(self):
        if self._handler:
            self._handler.cancel()
            self._handler = None
            # self._ctl.assign_external(parse_term('no_more_solutions'),False)
        self._iterator = None

    def _updateModel(self):
        try:
            self._model = ClinguinModel.fromWidgetsFile(
                self._ctl,
                self._widget_files, 
                self._assumptions,
                self._logger)
            # If option is active
            # self._model = self._modelClass.fromBCExtendedFile(self._ctl,self._assumptions, self._logger)
        except NoModelError:
            self._model.addMessage("Error","This operation can't be performed")

    def get(self):
        self._logger.debug("_get()")
        j=  StandardJsonEncoder.encode(self._model, self._logger)

        return j

    def clear(self):
        self._logger.debug("clear()")
        self._assumptions.clear()
        self._atoms.clear()
        self._endBrowsing()
        self._updateModel()
        return self.get()

    def assume(self, predicate):
        # Iconf
        self._logger.debug("assume(" + str(predicate) + ")")
        predicate_symbol = parse_term(predicate)
        if predicate_symbol not in self._assumptions:
            self._assumptions.add(predicate_symbol)
            self._endBrowsing()
            self._updateModel()
        return self.get()

    def removeAssume(self, predicate):
        # Iconf
        self._logger.debug("remove(" + str(predicate) + ")")
        predicate_symbol = parse_term(predicate)
        if predicate_symbol in self._assumptions:
            self._assumptions.remove(predicate_symbol)
            self._endBrowsing()
            self._updateModel()
        return self.get()
    
    # def removeAll(self, predicate):
        # Iconf

    # def setExternal

    def addAtom(self, predicate):
        self._logger.debug("addAtom(" + str(predicate) + ")")
        predicate_symbol = parse_term(predicate)
        if predicate_symbol not in self._atoms:
            self._atoms.add(predicate_symbol)
            # Maybe best to do using the callback tuple?
            self._initCtl()
            self._ground()
            self._endBrowsing()
            self._updateModel()
        return self.get()

    def removeAtom(self,predicate):
        self._logger.debug("remove(" + str(predicate) + ")")
        predicate_symbol = parse_term(predicate)
        if predicate_symbol in self._atoms:
            self._atoms.remove(predicate_symbol)
            self._initCtl()
            self._ground()
            self._endBrowsing()
            self._updateModel()
        return self.get()

    def nextSolution(self):
        self._logger.debug("nextSolution()")
        if not self._iterator:
            self._ctl.configuration.solve.enum_mode = 'auto'
            # Only if option
            # self._ctl.assign_external(parse_term('show_all'),True)
            self._handler = self._ctl.solve(
                assumptions=[(a,True) for a in self._assumptions],
                yield_=True)
            self._iterator = iter(self._handler)
        try:
            model = next(self._iterator)
            self._model = self._modelClass.fromClingoModel(model, self._logger)
        except StopIteration:
            self._logger.debug("No more solutions")
            self._handler.cancel()
            self._updateModel()
            self._model.addMessage("Browsing Information","No more solutions")

        return self.get()
