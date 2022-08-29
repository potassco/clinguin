from clinguin.server.data.clinguin_model import ClinguinModel
import networkx as nx
from typing import Sequence, Any
import argparse
import logging
import clingo
import textwrap

from clingo import Control, parse_term
from clingo.symbol import Function, Number, String


import clorm
import copy
import base64
from clorm import Raw

from clinguin.utils import StandardTextProcessing
from clinguin.server.data.attribute import AttributeDao



# Self defined
from clinguin.server import StandardJsonEncoder

from clinguin.server.application.default_backends.clingo_backend import ClingoBackend

from clinguin.server.application.default_backends.standard_utils.brave_cautious_helper import brave_cautious_externals
from clinguin.utils import NoModelError

from clingraph import Factbase, compute_graphs, render
from clingraph.clingo_utils import ClingraphContext



class ClingraphBackend(ClingoBackend):

    _intermediate_format = 'png'
    _encoding = 'utf-8'
    _attribute_image_key = 'image'
    _attribute_image_value = 'clingraph'
    _attribute_image_value_seperator = '__'

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

    def _computeClingraphGraphs(self,prg):
        fbs = []
        ctl = Control("0")
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

        return graphs

    def _saveClingraphGraphsToFile(self,graphs):
        if self._select_graph is not None:
            graphs = [{g_name:g for g_name, g in graph.items() if g_name in self._select_graph} for graph in graphs]
        write_arguments = {"directory":self._dir, "name_format":self._name_format}
        paths = render(graphs,
                format='png',
                engine=self._engine,
                view=False,
                **write_arguments)
        self._logger.debug("Clingraph saved images:")
        self._logger.debug(paths)

    
    def _getModelFilledWithBase64ImagesFromGraphs(self,graphs):
        model = self._model
        cls = self.__class__

        kept_symbols = list(model.getElements()) + list(model.getCallbacks())

        filled_attributes = []
    
        # TODO - Improve efficiency of filling attributes
        for attribute in model.getAttributes():
            if str(attribute.key) == cls._attribute_image_key:
                attribute_value = StandardTextProcessing.parseStringWithQuotes(str(attribute.value))

                if attribute_value.startswith(cls._attribute_image_value) and attribute_value != "clingraph":
                    splits = attribute_value.split(cls._attribute_image_value_seperator)
                    splits.pop(0)
                    rest = ""   
                    for split in splits:
                        rest = rest + split

                    base64_key_image = self._createImageFromGraph(graphs, key = rest)
                    filled_attributes.append(AttributeDao(Raw(Function(str(attribute.id),[])), Raw(Function(str(attribute.key),[])), Raw(String(str(base64_key_image)))))
                else:
                    filled_attributes.append(attribute)
            else:
                filled_attributes.append(attribute)

        return ClinguinModel(clorm.FactBase(copy.deepcopy(kept_symbols + filled_attributes)))


    def _createImageFromGraph(self, graphs, position = None, key = None):
        cls = self.__class__
        graphs = graphs[0]

        if position != None: 
            if (len(graphs)-1) >= position:
                graph = graphs[list(graphs.keys())[position]]
            else:
                self._logger.error("Attempted to access not valid position")
                raise Exception("Attempted to access not valid position")
        elif key != None:
            if key in graphs:
                graph = graphs[key]
            else:
                self._logger.error("Key not found in graphs: " + str(key))
                raise Exception("Key not found in graphs: " + str(key))
        else:
            self._logger.error("Must either specify position or key!")
            raise Exception("Must either specify position or key!")

        graph.format = cls._intermediate_format
        img = graph.pipe(engine=self._engine)

        encoded = base64.b64encode(img)
        decoded = encoded.decode(cls._encoding)

        return decoded        
        
    def _updateModel(self):
        super()._updateModel()
        try:
            prg = ClinguinModel.getCautiousBrave(self._ctl,self._assumptions)
            self._model = ClinguinModel.fromWidgetsFileAndProgram(self._ctl,self._widget_files,prg)

            graphs = self._computeClingraphGraphs(prg)

            self._saveClingraphGraphsToFile(graphs)

            self._filled_model = self._getModelFilledWithBase64ImagesFromGraphs(graphs)

        except NoModelError:
            self._model.addMessage("Error","This operation can't be performed")

    def get(self):
        json_structure = StandardJsonEncoder.encode(self._filled_model)
        return json_structure




