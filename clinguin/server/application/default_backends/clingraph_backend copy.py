import networkx as nx
from typing import Sequence, Any

import logging
import clingo
from clingo import Control, parse_term
from clingo.symbol import Function, Number, String

# Self defined
from clinguin.server import StandardJsonEncoder

from clinguin.server.data.clingraph_model import ClingraphModel

from clinguin.server import ClinguinBackend
from clinguin.server.application.default_backends.clingo_backend import ClingoBackend

from clinguin.server.application.default_backends.standard_utils.brave_cautious_helper import brave_cautious_externals
from clinguin.server.application.default_backends.clingraph_helper import clingraph_helper

class ClingraphBackend(ClingoBackend):

    def __init__(self, args):
        super(ClingoBackend, self).__init__(args)
        self._assumptions = set()
        self._images = set()

        self._files = args.source_files

        self._ctl = Control(['0'])
        for f in self._files:
            self._ctl.load(str(f))
        self._ctl.add("base",[],brave_cautious_externals)
        self._ctl.add("base",[],clingraph_helper)
        self._ctl.ground([("base", [])])
        self._ctl.assign_external(parse_term('show_all'),True)

        self._model=None
        self._semi_filled_model = None

        self._handler=None
        self._iterator=None
        
        self._modelClass = ClingraphModel
        self._graph_index = 0
        self._updateModelWithOptions()

    def _endBrowsing(self):
        if self._handler:
            self._handler.cancel()
            self._handler = None
            self._ctl.assign_external(parse_term('no_more_solutions'),False)
        self._iterator = None
        self._graph_index = 0


    def _updateModelWithOptions(self):
        self._semi_filled_model = self._modelClass.fromBCExtendedFile(self._ctl,self._assumptions, self._logger)
        self._graphs = self._semi_filled_model.solveGraphs()

        self._semi_filled_model = self._modelClass.fillClingraphNamedPlaceholders(self._logger, self._semi_filled_model, self._graphs)

        if (len(self._graphs) - 1) >= self._graph_index:
            self._model = self._modelClass.fillClingraphDefaultPlaceholders(self._logger, self._semi_filled_model, self._graphs, self._graph_index)
        else:
            self._model = self._semi_filled_model


    def nextGraph(self):
        self._logger.debug("nextGraph()")

        self._graph_index = self._graph_index + 1
        if (len(self._graphs) - 1) >= self._graph_index:
            self._model = self._modelClass.fillClingraphDefaultPlaceholders(self._logger, self._semi_filled_model, self._graphs, self._graph_index)
        else:
            self._logger.debug("No more graphs")
            self._ctl.assign_external(parse_term('no_more_graphs'), True)
            self._updateModelWithOptions()
        
        return self.get()


        
