# pylint: disable=R0801
"""
Module that contains the ClingraphBackend.
"""
import functools
import textwrap
from pathlib import Path

from clingo import Control
from clingo.symbol import Function, String
from clingraph import Factbase, compute_graphs
from clingraph.clingo_utils import ClingraphContext
from clorm import Raw

from clinguin.server.application.backends.clingo_backend import (
    ClingoBackend,
)
from clinguin.server.data.attribute import AttributeDao

# Self defined
from clinguin.utils import StandardTextProcessing, image_to_b64
from clinguin.utils.annotations import extends, overwrites

from ....utils.transformer import UsesSignatureTransformer


class ClingraphBackend(ClingoBackend):
    """
    Extends ClingoBackend. With this Backend it is possible to include clingraph images in the UI.
    The image is rendered based on a visualization encoding every time the UI is updated.
    Then, they are sent the client as Base64 encoding.
    """

    @extends(ClingoBackend)
    def _init_command_line(self):
        """
        Sets the arguments for computing clingraph images.
        """
        super()._init_command_line()
        # pylint: disable= attribute-defined-outside-init
        self._clingraph_files = self._args.clingraph_files
        self._select_model = self._args.select_model
        self._type = self._args.type
        self._select_graph = self._args.select_graph
        self._dir = self._args.dir
        self._name_format = self._args.name_format
        self._engine = self._args.engine

        self._intermediate_format = self._args.intermediate_format

        self._attribute_image_key = "image_type"
        self._attribute_image_value = "clingraph"

    # ---------------------------------------------
    # Class methods
    # ---------------------------------------------

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
            "--intermediate-format",
            default="svg",
            type=str,
            choices=[
                "png",
                "svg",
            ],
            help="Intermediate format. Use 'svg' for angular fronted and 'png' tkinter. (default: %(default)s)",
        )

    @functools.lru_cache(maxsize=None)  # pylint: disable=[method-cache-max-size-none]
    @overwrites(ClingoBackend)
    def _ui_uses_predicate(self, name: str, arity: int):
        """
        Returns a truth value of weather the ui_files contain the given signature.

        Args:
            name (str): Predicate name
            arity (int): Predicate arity
        """
        transformer = UsesSignatureTransformer(name, arity)
        self._logger.debug("Transformer parsing UI files to find %s/%s", name, arity)
        transformer.parse_files(self._ui_files + self._clingraph_files)
        return transformer.contained

    # ---------------------------------------------
    # UI update
    # ---------------------------------------------

    @extends(ClingoBackend)
    def _update_ui_state(self):
        """
        Updates the UI state by calling all domain state methods
        and creating a new control object (ui_control) using the ui_files provided
        """
        super()._update_ui_state()
        domain_state = self._domain_state
        graphs = self._compute_clingraph_graphs(domain_state)
        self._replace_uifb_with_b64_images_clingraph(graphs)

    # ---------------------------------------------
    # Private methods
    # ---------------------------------------------

    def _compute_clingraph_graphs(self, domain_state):
        """
        Computes all the graphs using the encoding and the domain state

        Arguments:

            domain_state (str): The model, brave, and cautious consequences (domain-state)
        """
        fbs = []
        ctl = Control("0")

        for f in self._clingraph_files:
            path = Path(f)
            if not path.is_file():
                self._logger.critical("File %s does not exist", f)
                raise Exception(f"File {f} does not exist")
            try:
                ctl.load(str(f))
            except Exception as e:
                self._logger.critical(
                    "Failed to load file %s (there is likely a syntax error in this logic program file).",
                    f,
                )
                raise e

        ctl.add("base", [], domain_state)
        ctl.ground([("base", [])], ClingraphContext())

        ctl.solve(on_model=lambda m: fbs.append(Factbase.from_model(m)))
        if self._select_model is not None:
            for m in self._select_model:
                if m >= len(fbs):
                    raise ValueError(f"Invalid model number selected {m}")
            fbs = [f if i in self._select_model else None for i, f in enumerate(fbs)]

        if len(fbs) > 1:
            self._logger.warning(
                "Multiple clingraph outputs were computed. Only first one considered."
            )
        graphs = compute_graphs([fbs[0]], graphviz_type=self._type)
        return graphs

    def _replace_uifb_with_b64_images_clingraph(self, graphs):
        """
        Replaces the clingraph predicates of the UI with the computed graphs.

        Arguments:
            graphs (dic) The computed graphs
        """
        attributes = list(self._ui_state.get_attributes(key=self._attribute_image_key))
        for attribute in attributes:
            attribute_value = StandardTextProcessing.parse_string_with_quotes(
                str(attribute.value)
            )
            is_cg_image = attribute_value.startswith(self._attribute_image_value)

            if not is_cg_image:
                continue

            graph_name = "default"
            split = attribute_value.split("__")
            if len(split) > 1:
                graph_name = split[1]

            image_value = self._create_image_from_graph(graphs, key=graph_name)
            new_image_key = "image"
            base64_key_image = image_to_b64(image_value)

            new_attribute = AttributeDao(
                Raw(Function(str(attribute.id), [])),
                Raw(Function(str(new_image_key), [])),
                Raw(String(str(base64_key_image))),
            )
            self._ui_state.add_attribute_direct(new_attribute)

    def _create_image_from_graph(self, graphs, position=None, key=None):
        """
        Creates the image of the graph using clingraph

        Arguments:
            graphs (dic) The computed graphs
            position (int) The position of the graph to show
            key (int) The key of the graph to show
        """
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
