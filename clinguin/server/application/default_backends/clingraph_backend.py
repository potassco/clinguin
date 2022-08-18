from clinguin.server.data.clinguin_model import ClinguinModel
import networkx as nx
from typing import Sequence, Any
import argparse
import logging
import clingo
import textwrap
from clingo import Control, parse_term
from clingo.symbol import Function, Number, String

# Self defined
from clinguin.server import StandardJsonEncoder

from clinguin.server.application.default_backends.clingo_backend import ClingoBackend

from clinguin.server.application.default_backends.standard_utils.brave_cautious_helper import brave_cautious_externals
from clinguin.utils import NoModelError

from clingraph import Factbase, compute_graphs, render
from clingraph.clingo_utils import ClingraphContext

class ClingraphBackend(ClingoBackend):

    def __init__(self, args):
        self._clingraph_files = args.clingraph_files
        self._select_model = args.select_model
        self._type = args.type
        self._select_graph = args.select_graph
        self._dir = args.dir
        self._name_format = args.name_format
        self._engine = args.engine
        super().__init__(args)

        

    @classmethod
    def registerOptions(cls, parser):     
        ClingoBackend.registerOptions(parser)

        parser.add_argument('--clingraph-files',
                        help = textwrap.dedent('''\
                            A visualization encoding that will be used to generate the graph facts
                            by calling clingo with the input.
                            This encoding is expected to have only one stable model.'''),
                        # type=argparse.FileType('r'),
                        nargs='+',
                        metavar='')

        parser.add_argument('--prefix',
                        default = '',
                        help = textwrap.dedent('''\
                            Prefix expected in all the considered facts.
                            Example: --prefix=viz_ will look for predicates named viz_node, viz_edge etc.'''),
                        type=str,
                        metavar='')

        parser.add_argument('--default-graph',
                        default = 'default',
                        help = textwrap.dedent('''\
                        The name of the default graph.
                        All nodes and edges with arity 1 will be assigned to this graph
                            (default: %(default)s)'''),
                        type=str,
                        metavar='')

        parser.add_argument('--select-graph',
                help = textwrap.dedent('''\
                    Select one of the graphs by name.
                    Can appear multiple times to select multiple graphs'''),
                type=str,
                action='append',
                nargs='?',
                metavar="")

        parser.add_argument('--select-model',
                help = textwrap.dedent('''\
                    Select only one of the models when using a json input.
                    Defined by a number starting in index 0.
                    Can appear multiple times to select multiple models.'''),
                type=int,
                action='append',
                nargs='?',
                metavar="")

        parser.add_argument('--name-format',
                    help = textwrap.dedent('''\
                        An optional string to format the name when saving multiple files,
                        this string can reference parameters `{graph_name}` and `{model_number}`.
                        Example `new_version-{graph_name}-{model_number}`
                        (default: `{graph_name}` or
                                `{model_number}/{graph_name}` for multi model functionality from json)'''),
                    type=str,
                    metavar='')

        parser.add_argument('--dir',
                        default = 'out',
                        help = textwrap.dedent('''\
                            Directory for writing the output files
                                (default: %(default)s)'''),
                        type=str,
                        metavar='')

        parser.add_argument('--type',
                    default = 'graph',
                    choices=['graph', 'digraph'],
                    help = textwrap.dedent('''\
                        The type of the graph
                        {graph|digraph}
                            (default: %(default)s)'''),
                    type=str,
                    metavar='')

        parser.add_argument('--engine',
                        default = 'dot',
                        choices=["dot","neato","twopi","circo","fdp","osage","patchwork","sfdp"],
                        help = textwrap.dedent('''\
                            Layout command used by graphviz
                            {dot|neato|twopi|circo|fdp|osage|patchwork|sfdp}
                                (default: %(default)s)'''),
                        type=str,
                        metavar="")



    def _compute_clingraph_graphs(self,prg):
        fbs = []
        ctl = Control([])
        for f in self._clingraph_files:
            ctl.load(f)
        ctl.add("base",[],prg)
        ctl.ground([("base",[])],ClingraphContext())
        ctl.solve(on_model=lambda m: fbs.append(Factbase.from_model(m)))
        if self._select_model is not None:
            for m in self._select_model:
                if m>=len(fbs):
                    raise ValueError(f"Invalid model number selected {m}")
            fbs = [f if i in self._select_model else None
                        for i, f in enumerate(fbs) ]
        graphs = compute_graphs(fbs, graphviz_type=self._type)
        if self._select_graph is not None:
            graphs = [{g_name:g for g_name, g in graph.items() if g_name in self._select_graph} for graph in graphs]
        write_arguments = {"directory":self._dir, "name_format":self._name_format}
        paths = render(graphs,
                format='png',
                engine=self._engine,
                view=False,
                **write_arguments)
        self._logger.debug(paths)
        
        
    def _updateModel(self):
        super()._updateModel()
        try:
            prg = ClinguinModel.getCautiosBrave(self._ctl,self._assumptions,self._logger)
            self._model = ClinguinModel.fromWidgetsFileAndProgram(self._ctl,self._widget_files,prg,self._logger)
            self._compute_clingraph_graphs(prg)
        except NoModelError:
            self._model.addMessage("Error","This operation can't be performed")