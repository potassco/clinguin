from clinguin.utils.errors import NoModelError
import networkx as nx
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

from standard_utils.brave_cautious_helper import *

class ClingoBackend(ClinguinBackend):

    def __init__(self, args):
        super().__init__(args)
        self._assumptions = set()
        self._atoms = set()
        self._files = args.source_files

        self.initClingo()

        self._ground()


        self._model=None
        self._handler=None
        self._iterator=None

        self._updateModelWithOptions()


    def initClingo(self):
        self._ctl = Control(['0'])
        for f in self._files:
            self._ctl.load(str(f))
        self._ctl.add("base",[],brave_cautious_externals)
    
    def _ground(self):
        self._ctl.ground([("base", [])])
        self._ctl.assign_external(parse_term('show_all'),True)


    @classmethod
    def registerOptions(cls, parser):
        parser.add_argument('source_files', nargs='+', help='Files')

    def _endBrowsing(self):
        if self._handler:
            self._handler.cancel()
            self._handler = None
            self._ctl.assign_external(parse_term('no_more_solutions'),False)
        self._iterator = None

    def _updateModelWithOptions(self):
        try:
            self._model = ClinguinModel.fromBCExtendedFile(self._ctl,self._assumptions)
        except NoModelError:
            self._model.addElement("message","message","window")
            self._model.addAttribute("message","title","Error")
            self._model.addAttribute("message","message","This operation can't be performed")

    def get(self):
        self._logger.info("assumptions:")
        self._logger.info(self._assumptions)
        self._logger.debug("_get()")
        j=  StandardJsonEncoder.encode(self._model)
        return j

    def assume(self, predicate):
        self._logger.debug("assume(" + str(predicate) + ")")
        predicate_symbol = parse_term(predicate)
        if predicate_symbol not in self._assumptions:
            self._assumptions.add(predicate_symbol)
            self._endBrowsing()
            self._updateModelWithOptions()
        return self.get()

    def solve(self):
        self._logger.debug("solve()")
        self._updateModelWithOptions()
        return self.get()

    def remove(self, predicate):
        self._logger.debug("remove(" + str(predicate) + ")")
        predicate_symbol = parse_term(predicate)
        if predicate_symbol in self._assumptions:
            self._assumptions.remove(predicate_symbol)
            self._endBrowsing()
            self._updateModelWithOptions()
        return self.get()
    
    def addAtom(self, predicate):
        self._logger.debug("addAtom(" + str(predicate) + ")")
        predicate_symbol = parse_term(predicate)
        if predicate_symbol not in self._atoms:
            self._atoms.add(predicate_symbol)

            self.initClingo()
            for atom in self._atoms:
                self._ctl.add("base",[],str(atom) + ".")
            self._ground()

            self._endBrowsing()
            self._updateModelWithOptions()
        return self.get()

    def removeAtom(self,predicate):
        self._logger.debug("remove(" + str(predicate) + ")")
        predicate_symbol = parse_term(predicate)
        if predicate_symbol in self._atoms:
            self._atoms.remove(predicate_symbol)

            self.initClingo()
            for atom in self._atoms:
                self._ctl.add("base",[],str(atom) + ".")
            self._ground()

            self._endBrowsing()
            self._updateModelWithOptions()
        return self.get()
        
            

    def removeAssume(self, predicate_remove, predicate_assume):
        self.remove(predicate_remove)
        return self.assume(predicate_assume)

    def clear(self):
        self._logger.debug("clear()")
        self._assumptions.clear()
        self._endBrowsing()
        self._updateModelWithOptions()
        return self.get()


    def nextSolution(self):
        self._logger.debug("nextSolution()")
        if not self._iterator:
            self._ctl.configuration.solve.enum_mode = 'auto'
            self._ctl.assign_external(parse_term('show_all'),True)
            self._handler = self._ctl.solve(
                assumptions=[(a,True) for a in self._assumptions],
                yield_=True)
            self._iterator = iter(self._handler)
        try:
            model = next(self._iterator)
            self._model = ClinguinModel.fromClingoModel(model)
        except StopIteration:
            self._logger.debug("No more solutions")
            self._handler.cancel()

            self._ctl.assign_external(parse_term('no_more_solutions'),True)
            self._updateModelWithOptions()

        return self.get()
