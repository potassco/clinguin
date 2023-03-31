"""
Module that contains the ClingraphBackend.
"""
import copy
import base64

import textwrap

from clingo import Control
from clingo.symbol import Function, String

import clorm
from clorm import Raw

from clingraph import Factbase, compute_graphs, render
from clingraph.clingo_utils import ClingraphContext

# Self defined
from clinguin.utils import StandardTextProcessing
from clinguin.server.data.attribute import AttributeDao
from clinguin.server.data.clinguin_model import ClinguinModel
from clinguin.server import StandardJsonEncoder
from clinguin.server.application.backends.clingo_backend import ClingoBackend
from clinguin.utils import NoModelError


class ClingraphBackend(ClingoBackend):
    """
    Extends ClingoBackend. With this Backend it is possible to create Clingraph-graphs by Clinguin. This can be done by both saving them to a file and by sending them to the client.
    The process of sending them to the client includes the conversion to a Base64 encoding (so the binary images are encoded as a UTF-8 String) that is then send to the client.
    """

    def __init__(self, args):
        super().__init__(args)

        self._clingraph_files = args.clingraph_files
        self._select_model = args.select_model
        self._type = args.type
        self._select_graph = args.select_graph
        self._dir = args.dir
        self._name_format = args.name_format
        self._engine = args.engine
        self._disable_saved_to_file = args.disable_saved_to_file

        self._intermediate_format = "png"
        self._encoding = "utf-8"
        self._attribute_image_key = "image"
        self._attribute_image_value = "clingraph"
        self._attribute_image_value_seperator = "__"

        self._filled_model = None

    # ---------------------------------------------
    # Overwrite
    # ---------------------------------------------

    def _update_model(self):
        try:
            prg = ClinguinModel.get_cautious_brave(self._ctl, self._assumptions)
            self._model = ClinguinModel.from_ui_file_and_program(
                self._ctl, self._ui_files, prg, self._assumptions
            )

            graphs = self._compute_clingraph_graphs(prg)

            if not self._disable_saved_to_file:
                self._save_clingraph_graphs_to_file(graphs)

            self._filled_model = self._get_mode_filled_with_base_64_images_from_graphs(
                graphs
            )

        except NoModelError:
            self._model.add_message("Error", "This operation can't be performed")

    def get(self):
        """
        Overwritten from ClingoBackend. Difference: Converts the _filled_model to Json instead of the _model, as the _filled_model contains the Base64 encoded images.
        """
        if not self._filled_model:
            self._update_model()

        json_structure = StandardJsonEncoder.encode(self._filled_model)
        return json_structure

    @classmethod
    def register_options(cls, parser):
        """
        Registers command line options for ClingraphBackend.
        """
        ClingoBackend.register_options(parser)

        parser.add_argument(
            "--clingraph-files",
            help=textwrap.dedent(
                """\
                            A visualization encoding that will be used to generate the graph facts
                            by calling clingo with the input.
                            This encoding is expected to have only one stable model."""
            ),
            # type=argparse.FileType('r'),
            nargs="+",
            metavar="",
        )

        parser.add_argument(
            "--prefix",
            default="",
            help=textwrap.dedent(
                """\
                            Prefix expected in all the considered facts.
                            Example: --prefix=viz_ will look for predicates named viz_node, viz_edge etc."""
            ),
            type=str,
            metavar="",
        )

        parser.add_argument(
            "--default-graph",
            default="default",
            help=textwrap.dedent(
                """\
                        The name of the default graph.
                        All nodes and edges with arity 1 will be assigned to this graph
                            (default: %(default)s)"""
            ),
            type=str,
            metavar="",
        )

        parser.add_argument(
            "--select-graph",
            help=textwrap.dedent(
                """\
                    Select one of the graphs by name.
                    Can appear multiple times to select multiple graphs"""
            ),
            type=str,
            action="append",
            nargs="?",
            metavar="",
        )

        parser.add_argument(
            "--select-model",
            help=textwrap.dedent(
                """\
                    Select only one of the models when using a json input.
                    Defined by a number starting in index 0.
                    Can appear multiple times to select multiple models."""
            ),
            type=int,
            action="append",
            nargs="?",
            metavar="",
        )

        parser.add_argument(
            "--name-format",
            help=textwrap.dedent(
                """\
                        An optional string to format the name when saving multiple files,
                        this string can reference parameters `{graph_name}` and `{model_number}`.
                        Example `new_version-{graph_name}-{model_number}`
                        (default: `{graph_name}` or
                                `{model_number}/{graph_name}` for multi model functionality from json)"""
            ),
            type=str,
            metavar="",
        )

        parser.add_argument(
            "--dir",
            default="out",
            help=textwrap.dedent(
                """\
                            Directory for writing the output files
                                (default: %(default)s)"""
            ),
            type=str,
            metavar="",
        )

        parser.add_argument(
            "--type",
            default="graph",
            choices=["graph", "digraph"],
            help=textwrap.dedent(
                """\
                        The type of the graph
                        {graph|digraph}
                            (default: %(default)s)"""
            ),
            type=str,
            metavar="",
        )

        parser.add_argument(
            "--engine",
            default="dot",
            choices=[
                "dot",
                "neato",
                "twopi",
                "circo",
                "fdp",
                "osage",
                "patchwork",
                "sfdp",
            ],
            help=textwrap.dedent(
                """\
                            Layout command used by graphviz
                            {dot|neato|twopi|circo|fdp|osage|patchwork|sfdp}
                                (default: %(default)s)"""
            ),
            type=str,
            metavar="",
        )

        parser.add_argument(
            "--disable-saved-to-file",
            action="store_true",
            help="Disable image saved to file",
        )

    # ---------------------------------------------
    # Private methods
    # ---------------------------------------------

    def _compute_clingraph_graphs(self, prg):
        fbs = []
        ctl = Control("0")
        for f in self._clingraph_files:
            ctl.load(f)
        ctl.add("base", [], prg)
        ctl.ground([("base", [])], ClingraphContext())

        ctl.solve(on_model=lambda m: fbs.append(Factbase.from_model(m)))
        if self._select_model is not None:
            for m in self._select_model:
                if m >= len(fbs):
                    raise ValueError(f"Invalid model number selected {m}")
            fbs = [f if i in self._select_model else None for i, f in enumerate(fbs)]

        graphs = compute_graphs(fbs, graphviz_type=self._type)

        return graphs

    def _save_clingraph_graphs_to_file(self, graphs):
        if self._select_graph is not None:
            graphs = [
                {
                    g_name: g
                    for g_name, g in graph.items()
                    if g_name in self._select_graph
                }
                for graph in graphs
            ]
        write_arguments = {"directory": self._dir, "name_format": self._name_format}
        paths = render(
            graphs, format="png", engine=self._engine, view=False, **write_arguments
        )
        self._logger.debug("Clingraph saved images:")
        self._logger.debug(paths)

    def _get_mode_filled_with_base_64_images_from_graphs(self, graphs):
        model = self._model

        kept_symbols = list(model.get_elements()) + list(model.get_callbacks())

        filled_attributes = []

        # TODO - Improve efficiency of filling attributes
        for attribute in model.get_attributes():
            if str(attribute.key) == self._attribute_image_key:
                attribute_value = StandardTextProcessing.parse_string_with_quotes(
                    str(attribute.value)
                )

                if (
                    attribute_value.startswith(self._attribute_image_value)
                    and attribute_value != "clingraph"
                ):
                    splits = attribute_value.split(
                        self._attribute_image_value_seperator
                    )
                    splits.pop(0)
                    rest = ""
                    for split in splits:
                        rest = rest + split

                    key_image = self._create_image_from_graph(graphs, key=rest)

                    base64_key_image = self._convertImageToBase64String(key_image)

                    filled_attributes.append(
                        AttributeDao(
                            Raw(Function(str(attribute.id), [])),
                            Raw(Function(str(attribute.key), [])),
                            Raw(String(str(base64_key_image))),
                        )
                    )
                else:
                    filled_attributes.append(attribute)
            else:
                filled_attributes.append(attribute)

        return ClinguinModel(
            clorm.FactBase(copy.deepcopy(kept_symbols + filled_attributes))
        )

    def _create_image_from_graph(self, graphs, position=None, key=None):
        graphs = graphs[0]

        if position is not None:
            if (len(graphs) - 1) >= position:
                graph = graphs[list(graphs.keys())[position]]
            else:
                self._logger.error("Attempted to access not valid position")
                raise Exception("Attempted to access not valid position")
        elif key is not None:
            if key in graphs:
                graph = graphs[key]
            else:
                self._logger.error("Key not found in graphs: %s", str(key))
                raise Exception("Key not found in graphs: " + str(key))
        else:
            self._logger.error("Must either specify position or key!")
            raise Exception("Must either specify position or key!")

        graph.format = self._intermediate_format
        img = graph.pipe(engine=self._engine)

        return img

    def _convertImageToBase64String(self, img):
        encoded = base64.b64encode(img)
        decoded = encoded.decode(self._encoding)
        return decoded
