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

from clinguin.server.application.default_backends.clingo_backend import ClingoBackend


from clinguin.server.application.default_backends.standard_utils.brave_cautious_helper import *

class TemporalBackend(ClingoBackend):

    def __init__(self, args):
        self._step = 1
        self._last_grounded_step = 0
        self._full_plan=None
        super().__init__(args)
        

    def _initCtl(self):
        self._step= 1
        self._last_grounded_step= 0
        self._full_plan=None
        super()._initCtl()

    def _ground(self):
        if not self._last_grounded_step:
            self._ctl.ground([("base", [])])
        while self._step>self._last_grounded_step:
            self._last_grounded_step+=1
            self._ctl.ground([("step", [Number(self._step)])])
        if self._step>1:
            self._ctl.assign_external(Function('query',[Number(self._step-1)]),False)
        self._ctl.assign_external(Function('query',[Number(self._step)]),True)


    def _findIncrementally(self):
        if self._step>1:
            self._ctl.assign_external(Function('check',[Number(self._step-1)]),False)
        self._ctl.assign_external(Function('check',[Number(self._step)]),True)
        plan = self._findPlan()
        
        while plan == None or self._step>100:
            self._step +=1
            self._ground()
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


    def findPlan(self):
        if not self._full_plan:
            self._findIncrementally()

        symbols = "\n".join([str(s)+"." for s in self._full_plan])
        wctl = ClinguinModel.wid_control(self._widget_files,symbols)
        self._model = ClinguinModel.fromCtl(wctl)
        return self.get()

    def assumeAndStep(self, predicate):
        predicate_symbol = parse_term(predicate)
        self._assumptions.add(predicate_symbol)
        self._step +=1
        self._ground()
        self._endBrowsing()
        self._updateModel()
        return self.get()

    def removeAssumption(self, predicate):
        raise NotImplementedError()

    """
    def addAtom(self, predicate):
        raise NotImplementedError()


    def removeAtom(self,predicate):
        raise NotImplementedError()
    """

    def nextSolution(self):
        raise NotImplementedError()
