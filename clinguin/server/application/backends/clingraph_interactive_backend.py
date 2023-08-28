# pylint: disable=R0801,C0103,E1123,R0912,R0915,R1705
"""
Module that packs the clingraph interactive backend.
TODO -> Integrate this functionality to normal clingraph backend.
"""
import textwrap
import base64

from pathlib import Path
from clingo import Control
from clorm.clingo import Control as ClormControl
from clingo import Control, parse_term

from clinguin.server import ClinguinBackend
from clinguin.server.application.backends import ClingoBackend
from clinguin.server import StandardJsonEncoder

from clingraph import Factbase, compute_graphs, render
from clingraph.clingo_utils import ClingraphContext

from .standard_utils.clingo_logger import ClingoLogger
from .standard_utils.interactivity_options_contexts import (
    Option_Context,
    OptionsList,
    Select_Option,
    createOptionsList,
)

from clinguin.utils import StandardTextProcessing

from clinguin.server.data.attribute import AttributeDao


class ClingraphInteractiveBackend(ClingoBackend):
    """
    ClingraphInteractiveBackend class.
    """

    def __init__(self, args):
        super().__init__(args)

        self._options_encoding_files = args.options_encoding
        self._clingraph_files = args.clingraph_files

        self._select_model = args.select_model
        self._type = args.type
        self._select_graph = args.select_graph
        self._dir = args.dir
        self._name_format = args.name_format
        self._engine = args.engine
        self._disable_saved_to_file = args.disable_saved_to_file

        self._intermediate_format = "svg"
        self._encoding = "utf-8"
        self._attribute_image_key = "image"
        self._attribute_image_value = "clingraph"
        self._attribute_image_value_seperator = "__"

        self._graphs = None

    @classmethod
    def register_options(cls, parser):
        """
        Register specific arguments.
        """

        parser.add_argument("--domain-files", nargs="+", help="Files", metavar="")

        parser.add_argument(
            "--ui-files", nargs="+", help="Files for the element generation", metavar=""
        )

        parser.add_argument(
            "--clingraph-files",
            help=textwrap.dedent(
                """\
                            A visualization encoding that will be used to generate the graph facts
                            by calling clingo with the input.
                            This encoding is expected to have only one stable model."""
            ),
            nargs="+",
            metavar="",
        )

        parser.add_argument(
            "--options-encoding",
            help="Encoding for the options, must return facts of type option_context/5",
            nargs=1,
        )

        parser.add_argument(
            "-c",
            "--const",
            nargs="+",
            help="Constant passed to clingo, <id>=<term> replaces term occurrences of <id> with <term>",
            metavar="",
        )
        parser.add_argument(
            "--include-menu-bar",
            action="store_true",
            help="Inlcude a menu bar with options: Next, Select and Clear",
        )
        parser.add_argument(
            "--ignore-unsat-msg",
            action="store_true",
            help="The automatic pop-up message in the UI when the domain files are UNSAT, will be ignored.",
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

    def graphUpdate(self, *kwargs):

        if kwargs[0] != "":

            self._atoms = set()

            for arg in kwargs:
                predicate_symbol = parse_term(arg)
                if predicate_symbol not in self._atoms:
                    self._atoms.add(predicate_symbol)


            self._init_ctl()
            self._ground()
            self._end_browsing()
            self._update_uifb()

            self._logger.debug(self._uifb)
            json_structure = StandardJsonEncoder.encode(self._uifb)

            looked_upon_elements = [json_structure]
            while len(looked_upon_elements) > 0:
                element = looked_upon_elements.pop(0)
                looked_upon_elements = looked_upon_elements + element.children

                if element.type == "clingraph_interactive":
                    raw = self.graphUpdateHelper()
                    element.attributes.append(raw)

        return json_structure
   
    def get(self):
        """
        The get method.
        """

        if self._uifb.is_empty:
            self._update_uifb()

        self._logger.debug(self._uifb)
        json_structure = StandardJsonEncoder.encode(self._uifb)

        looked_upon_elements = [json_structure]
        while len(looked_upon_elements) > 0:
            element = looked_upon_elements.pop(0)
            looked_upon_elements = looked_upon_elements + element.children

            if element.type == "clingraph_interactive":
                raw = self.graphUpdateHelper()
                element.attributes.append(raw)

        return json_structure

    def _update_uifb_ui(self):
        super()._update_uifb_ui()
        if self._uifb.is_unsat:
            return
        self._graphs = self._compute_clingraph_graphs(self._uifb.conseq_facts)

    def graphUpdateHelper(self):
        """
        Updates the graph and returns it.
        """

        svg_image = self._generate_svg_image(self._graphs)
        options_list = self._generate_options_list()

        raw = {"key":"clingraph_interactive", "value":"", "data": svg_image, "option_data": options_list.to_json()}
        return raw
    
    def _generate_options_list(self):
        fbs = []

        clorm_ctl = ClormControl(
            unifier=[Option_Context, Select_Option], logger=ClingoLogger.logger
        )

        existant_file_counter = 0
        for f in self._options_encoding_files:
            path = Path(f)
            if path.is_file():
                try:
                    clorm_ctl.load(str(f))
                    existant_file_counter += 1
                except Exception:
                    self._logger.critical(
                        "Failed to load file %s (there is likely a syntax error in this logic program file).",
                        f,
                    )
            else:
                self._logger.critical(
                    "File %s does not exist, this file is skipped.", f
                )

        if existant_file_counter == 0:
            exception_string = (
                "None of the provided options encoding files exists, but at least one syntactically"
                + "valid options encoding file must be specified. Exiting!"
            )

            self._logger.critical(exception_string)
            raise Exception(exception_string)

        clorm_ctl.add("base", [], self._uifb.conseq_facts)
        clorm_ctl.add("base", [], self._backend_state_prg)

        clorm_ctl.ground([("base", [])])

        clorm_ctl.solve(on_model=lambda m: fbs.append(Factbase.from_model(m)))

        options_models = []

        with clorm_ctl.solve(yield_=True) as handle:
            for model in handle:
                facts = model.facts(atoms=True, terms=True)
                options_models.append(facts)
                break

        if len(options_models) <= 0:
            return Exception(
                "Could not solve your options encoding with your program output. No options will be displayed"
            )
        

        options_list: OptionsList = createOptionsList(options_models[0])
        return options_list

    

    def _compute_clingraph_graphs(self, prg):
        fbs = []
        ctl = Control("0")

        existant_file_counter = 0
        for f in self._clingraph_files:
            path = Path(f)
            if path.is_file():
                try:
                    ctl.load(str(f))
                    existant_file_counter += 1
                except Exception:
                    self._logger.critical(
                        "Failed to load file %s (there is likely a syntax error in this logic program file).",
                        f,
                    )
            else:
                self._logger.critical(
                    "File %s does not exist, this file is skipped.", f
                )

        if existant_file_counter == 0:
            exception_string = (
                "None of the provided clingraph files exists, but at least one syntactically"
                + "valid clingraph file must be specified. Exiting!"
            )

            self._logger.critical(exception_string)
            raise Exception(exception_string)

        ctl.add("base", [], prg)
        ctl.add("base", [], self._backend_state_prg)
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

    def _generate_svg_image(self, graphs):
        attributes = list(self._uifb.get_attributes())
        for attribute in attributes:
            if str(attribute.key) != self._attribute_image_key:
                continue
            attribute_value = StandardTextProcessing.parse_string_with_quotes(
                str(attribute.value)
            )
            is_cg_image = (
                attribute_value.startswith(self._attribute_image_value)
                and attribute_value != "clingraph"
            )
            if not is_cg_image:
                continue
            splits = attribute_value.split(self._attribute_image_value_seperator, 1)
            if len(splits) < 2:
                raise ValueError(
                    f"The images for clingraph should have format {self._attribute_image_value}"
                    + f"{self._attribute_image_value_seperator}name"
                )
            graph_name = splits[1]
            key_image = self._create_image_from_graph(graphs, key=graph_name)

            """
            base64_key_image = self._image_to_b64(key_image)
            new_attribute = AttributeDao(
                Raw(Function(str(attribute.id), [])),
                Raw(Function(str(attribute.key), [])),
                Raw(String(str(base64_key_image))),
            )
            self._uifb.replace_attribute(attribute, new_attribute)

            """

            return key_image

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

    def _image_to_b64(self, img):
        encoded = base64.b64encode(img)
        decoded = encoded.decode(self._encoding)
        return decoded

