from clinguin.server.application.clinguin_backend import ClinguinBackend
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


class TemporalBackend(ClinguinBackend):
    
    def __init__(self, args):
        super().__init__(args)
        self._assumptions = set()
        self._atoms = set()
        self._files = args.source_files
        self._wfiles = args.widget_files

        
        self._step = 1
        self._model=None
        self._full_plan=None
        self._initClingo()
        self._groundStep()
        self._updateModelWithOptions()


    def _initClingo(self):
        self._ctl = Control(['0'])
        for f in self._files:
            self._ctl.load(str(f))
        self._ctl.ground([("base", [])])

    @classmethod
    def registerOptions(cls, parser):
        parser.add_argument('--source-files', nargs='+', help='Files')
        parser.add_argument('--widget-files', nargs='+', help='Files for the widget generation')

    def _groundStep(self):
        self._ctl.ground([("step", [Number(self._step)])])
        if self._step>1:
            self._ctl.assign_external(Function('query',[Number(self._step-1)]),False)
        self._ctl.assign_external(Function('query',[Number(self._step)]),True)

    def _updateModelWithOptions(self):
        self._model = ClinguinModel.fromWidgetsFile(
                self._ctl,
                self._wfiles, 
                self._assumptions)



    def _findIncrementally(self):
        if self._step>1:
            self._ctl.assign_external(Function('check',[Number(self._step-1)]),False)
        self._ctl.assign_external(Function('check',[Number(self._step)]),True)
        plan = self._findPlan()
        
        while plan == None or self._step>100:
            self._step +=1
            self._groundStep()
            if self._step>1:
                self._ctl.assign_external(Function('check',[Number(self._step-1)]),False)
            self._ctl.assign_external(Function('check',[Number(self._step)]),True)
            plan = self._findPlan()

        if self._full_plan == None:
            raise RuntimeError(f"No plan found before 100 steps")


        return self._full_plan

    def _findPlan(self):
        self._ctl.configuration.solve.enum_mode = 'auto'
        hdn = self._ctl.solve(
            assumptions=[(a,True) for a in self._assumptions],
            yield_=True)
        itr = iter(hdn)
        try:
            model = next(itr)
            self._full_plan = model.symbols(atoms=True)
            hdn.cancel()
        except StopIteration:
            hdn.cancel()
            self._full_plan=None
        
        return self._full_plan

    # -------- Endpoints 
    
    def get(self):
        j=  StandardJsonEncoder.encode(self._model, self._logger)
        return j

    def assume(self, predicate):
        self._logger.debug("assume(" + str(predicate) + ")")
        predicate_symbol = parse_term(predicate)
        self._assumptions.add(predicate_symbol)
        self._step +=1
        self._groundStep()
        self._updateModelWithOptions()
        return self.get()

    def externalTrue(self, predicate):
        self._logger.debug("external(" + str(predicate) + ")")
        self._ctl.assign_external(parse_term(predicate),True)
        self._updateModelWithOptions()
        return self.get()


    def findPlan(self):
        if not self._full_plan:
            self._findIncrementally()

        symbols = "\n".join([str(s)+"." for s in self._full_plan])
        wctl = ClinguinModel.wid_control(self._wfiles,symbols)

        self._model = ClinguinModel.fromCtl(wctl)
       
        return self.get()
