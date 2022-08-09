import networkx as nx
from typing import Sequence, Any

import logging
import clingo
from clingo import Control, parse_term
from clingo.symbol import Function, Number, String

from clinguin.server.application.standard_json_encoder import StandardJsonEncoder

from clinguin.server.data.clinguin_model import ClinguinModel

from clinguin.server.application.clinguin_backend import ClinguinBackend

from clinguin.server.application.default_solvers.brave_cautious_helper import *

from clinguin.server.data.element import ElementDao
from clinguin.server.data.attribute import AttributeDao
from clinguin.server.data.callback import CallbackDao

class ClingoBackend(ClinguinBackend):

    def __init__(self, args):
        super().__init__(args)
        self._assumptions = set()
        self._files = args.source_files

        self._ctl = Control(['0'])
        for f in self._files:
            self._ctl.load(str(f))
        self._ctl.add("base",[],brave_cautious_externals)
        self._ctl.ground([("base", [])])
        self._ctl.assign_external(parse_term('show_all'),True)

        self._model=None
        self._handler=None
        self._iterator=None

        self._updateModelWithOptions()


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
        self._model = ClinguinModel.fromBCExtendedFile(self._ctl,self._assumptions)

    def get(self):
        self._logger.debug("_get()")
        # print(self._model)
        # Your old approach would now be this:
        # brave_model = ClinguinModel.fromBraveModel(self._ctl,self._assumptions)
        # brave_model.filterElements(lambda w: str(w.type) == 'dropdownmenuitem')
        # cautious_model = ClinguinModel.fromCautiousModel(self._ctl,self._assumptions)
        # model=ClinguinModel.combine(brave_model,cautious_model)
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
