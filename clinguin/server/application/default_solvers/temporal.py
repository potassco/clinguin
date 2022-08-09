import networkx as nx
from typing import Sequence, Any

import logging
import clingo
from clingo import Control, parse_term
from clingo.symbol import Function, Number, String

from clinguin.server import StandardJsonEncoder
from clinguin.server import ClinguinModel
from clinguin.server import ClinguinBackend

from standard_utils.brave_cautious_helper import *

class Temporal(ClinguinBackend):

    def __init__(self, args):
        super().__init__(args)

    @classmethod
    def registerOptions(cls, parser):
        parser.add_argument('source_files', nargs='+', help='Files')

    def _get(self):
        pass
