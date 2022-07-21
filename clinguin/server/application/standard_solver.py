import networkx as nx
from typing import Sequence, Any

import logging

from clinguin.server.application.standard_json_encoder import StandardJsonEncoder

from clinguin.server.data.clinguin_model import ClinguinModel

# Like an interface
class ClinguinBackend:
    
    def __init__(self, parsed_config):
        self._logger = logging.getLogger(parsed_config['logger']['server']['name'])
        self._parsed_config = parsed_config

    @classmethod
    def _registerOptions(cls, parser):
        pass

    def _get(self):
        pass

class ClingoBackend(ClinguinBackend):

    def __init__(self, parsed_config, files):
        super().__init__(parsed_config)
        self._assumptions = set()
        self._files = files
   
    """
    # TODO 
    @classmethod
    def _registerOptions(cls, parser):
        parser.add_argument('files', nargs = '+', help = 'Files')
        # any argument passsed here will be passed to the init on creation
        return ["files"] 
        # clinguin server -h
        # server --   
        # ClingoBackend:
        #     files: laksjsakds

        # ConfigBackend:
        #      name: sss

        # clinguin server --server=ClingoBackend filesl
        # clinguin server --server=ConfigBackend --name

        # clinguin client -h
        # server --   
        # TkinterUI:
        #     ksjaksjfklsa s s
    """
        


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

