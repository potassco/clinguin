import networkx as nx
from typing import Sequence, Any

import logging
import clingo
from clingo import Control
from clingo.symbol import Function, Number, String

from clinguin.server.application.standard_json_encoder import StandardJsonEncoder

from clinguin.server.data.clinguin_model import ClinguinModel

from clinguin.server.application.clinguin_backend import ClinguinBackend


class ClingoBackend(ClinguinBackend):

    def __init__(self, args):
        super().__init__(args)
        self._assumptions = set()
        self._files = args.source_files

        self._ctl = Control()
        for f in self._files:
            self._ctl.load(str(f))
        self._ctl.ground([("base", [])])

    @classmethod
    def registerOptions(cls, parser):
        parser.add_argument('source_files', nargs='+', help='Files')

    # becomes an endpoint option is the basic default one! instead of solve
    # just get
    def get(self):
        self._logger.debug("_get()")

        model = ClinguinModel(self._files, self._logger)
        model.computeCautious(self._ctl, self._assumptions, lambda w: True)
        model.computeBrave(
            self._ctl, self._assumptions, lambda w: str(
                w.type) == 'dropdownmenuitem')

        self._logger.debug("will encode")
        return StandardJsonEncoder.encode(model)

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
