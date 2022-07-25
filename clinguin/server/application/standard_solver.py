import networkx as nx
from typing import Sequence, Any

import logging

from clinguin.server.application.standard_json_encoder import StandardJsonEncoder

from clinguin.server.data.clinguin_model import ClinguinModel

from clinguin.server.application.clinguin_backend import ClinguinBackend

class ClingoBackend(ClinguinBackend):

    def __init__(self, parsed_config, args_dict):
        super().__init__(parsed_config)
        self._assumptions = set()
        self._files = args_dict['source_files']
   
    @classmethod
    def _registerOptions(cls, parser):
        parser.add_argument('source_files', nargs = '+', help = 'Files')

    # becomes an endpoint option is the basic default one! instead of solve just get
    def _get(self):
        self._logger.debug("_get()")
        
        model = ClinguinModel(self._files, self._parsed_config)
        model.computeCautious(self._assumptions, lambda w: True)
        model.computeBrave(self._assumptions, lambda w : str(w.type) == 'dropdownmenuitem')

        return StandardJsonEncoder.encode(model)

    # becomes an endpoint option
    def assume(self, predicate):
        self._logger.debug("assume(" + str(predicate) + ")")
        if predicate not in self._assumptions:
            self._assumptions.add(predicate)
        return self._get()
    
    # becomes an endpoint option
    def solve(self):
        self._logger.debug("solve()")
        self.model = None
        return self._get()

    # becomes an endpoint option
    def remove(self, predicate):
        self._logger.debug("remove(" + str(predicate) + ")")
        if predicate in self._assumptions:
            self._assumptions.remove(predicate)
            self._assumptions.remove("assume(" + predicate + ")")
            self.model=None
        return self._get()

