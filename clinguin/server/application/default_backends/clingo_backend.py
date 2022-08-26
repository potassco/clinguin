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
        self._source_files = args.source_files
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
        parser.add_argument('--source-files', nargs='+', help='Files',metavar='')
        parser.add_argument('--widget-files', nargs='+', help='Files for the widget generation',metavar='')

    def _restart(self):
        self._endBrowsing()
        self._assumptions = set()
        self._externals = {"true":set(),"false":set(),"released":set()}
        self._atoms = set()
        self._initCtl()
        self._ground()

    def _initCtl(self):
        self._ctl = Control(['0'])
        for f in self._source_files:
            try:
                self._ctl.load(str(f))
            except Exception as e:
                self._logger.critical(str(e))
                self._logger.critical("Failed to load modules (there is likely a syntax error in your logic program), now exiting - see previous stack trace for more information.")
                sys.exit()
        
        for atom in self._atoms:
            self._ctl.add("base",[],str(atom) + ".")
        
        
    
    def _ground(self):
        self._ctl.ground([("base", [])])

    
    def _endBrowsing(self):
        if self._handler:
            self._handler.cancel()
            self._handler = None
        self._iterator = None

    def _updateModel(self):
        try:
            self._model = ClinguinModel.fromWidgetsFile(
                self._ctl,
                self._widget_files, 
                self._assumptions)
        except NoModelError:
            self._model.addMessage("Error","This operation can't be performed")

    def get(self):
        json_structure =  StandardJsonEncoder.encode(self._model)

        return json_structure

    def clearAssumptions(self):
        self._endBrowsing()
        self._assumptions = set()
        self._initCtl()
        self._ground()

        self._updateModel()
        return self.get()

    def addAssumption(self, predicate):
        # Iconf
        predicate_symbol = parse_term(predicate)
        if predicate_symbol not in self._assumptions:
            self._assumptions.add(predicate_symbol)
            self._endBrowsing()
            self._updateModel()
        return self.get()

    def removeAssumption(self, predicate):
        # Iconf
        predicate_symbol = parse_term(predicate)
        if predicate_symbol in self._assumptions:
            self._assumptions.remove(predicate_symbol)
            self._endBrowsing()
            self._updateModel()
        return self.get()
   
    def clearAtoms(self):
        #self._restart()
        self._endBrowsing()
        self._atoms = set()
        self._initCtl()
        self._ground()

        self._updateModel()
        return self.get()

    def addAtom(self, predicate):
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
        predicate_symbol = parse_term(predicate)
        if predicate_symbol in self._atoms:
            self._atoms.remove(predicate_symbol)
            self._initCtl()
            self._ground()
            self._endBrowsing()
            self._updateModel()
        return self.get()

    def setExternal(self, predicate, value):
        symbol = parse_term(predicate)
        name = value

        if name == "release":
            self._ctl.release_external(parse_term(predicate))
            self._externals["released"].add(symbol)

            if symbol in self._externals["true"]:
                self._externals["true"].remove(symbol)
    
            if symbol in self._externals["false"]:
                self._externals["false"].remove(symbol)

        elif name == "true":
            self._ctl.assign_external(parse_term(predicate),True)
            self._externals["true"].add(symbol)

            if symbol in self._externals["false"]:
                self._externals["false"].remove(symbol)

        elif name == "false":
            self._ctl.assign_external(parse_term(predicate),True)
            self._externals["false"].add(symbol)

            if symbol in self._externals["true"]:
                self._externals["true"].remove(symbol)

        else:
            raise ValueError(f"Invalid external value {name}. Must be true, false or relase")

        self._updateModel()
        return self.get()

    def nextSolution(self):
        if not self._iterator:
            self._ctl.configuration.solve.enum_mode = 'auto'
            self._handler = self._ctl.solve(
                assumptions=[(a,True) for a in self._assumptions],
                yield_=True)
            self._iterator = iter(self._handler)
        try:
            model = next(self._iterator)
            self._model = self._modelClass.fromClingoModel(model)
        except StopIteration:
            self._logger.info("No more solutions")
            self._handler.cancel()
            self._updateModel()
            self._model.addMessage("Browsing Information","No more solutions")

        return self.get()
