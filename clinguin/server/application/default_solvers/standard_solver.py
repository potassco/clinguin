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

class ClingoBackend(ClinguinBackend):

    def __init__(self, args):
        super().__init__(args)
        self._assumptions = set()
        self._files = args.source_files

        self._ctl = Control()
        for f in self._files:
            self._ctl.load(str(f))
        self._ctl.add("base",[],brave_cautious_externals)
        self._ctl.ground([("base", [])])

        self._ctl.assign_external(parse_term('show_untagged'),True)


    @classmethod
    def registerOptions(cls, parser):
        parser.add_argument('source_files', nargs='+', help='Files')

    # becomes an endpoint option is the basic default one! instead of solve
    # just get
    def get(self):
        self._logger.debug("_get()")

        model = ClinguinModel.fromBCExtendedFile(self._ctl,self._assumptions)
        
        # Your old approach would now be this:
        # brave_model = ClinguinModel.fromBraveModel(self._ctl,self._assumptions)
        # brave_model.filterElements(lambda w: str(w.type) == 'dropdownmenuitem')
        # cautious_model = ClinguinModel.fromCautiousModel(self._ctl,self._assumptions)
        # model=ClinguinModel.combine(brave_model,cautious_model)


        self._logger.debug("will encode")
        j =  StandardJsonEncoder.encode(model)
        self._logger.debug("encoded")
        return j

    # becomes an endpoint option
    def assume(self, predicate):
        self._logger.debug("assume(" + str(predicate) + ")")
        if predicate not in self._assumptions:
            self._assumptions.add(predicate)
        return self.get()

    # becomes an endpoint option
    def solve(self):
        self._logger.debug("solve()")
        self.model = None
        return self.get()

    # becomes an endpoint option
    def remove(self, predicate):
        self._logger.debug("remove(" + str(predicate) + ")")
        if predicate in self._assumptions:
            self._assumptions.remove(predicate)
            self._assumptions.remove("assume(" + predicate + ")")
            self.model = None
        return self.get()

    def clear(self):
        self._logger.debug("clear()")
        self._assumptions.clear()
        return self.get()


