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

class Temporal(ClinguinBackend):

    def __init__(self, args):
        super().__init__(args)

    @classmethod
    def registerOptions(cls, parser):
        parser.add_argument('source_files', nargs='+', help='Files')

    def _get(self):
        pass
