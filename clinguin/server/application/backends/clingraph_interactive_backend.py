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
from clinguin.server.application.backends import ClingoBackend, ClingraphBackend
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


class ClingraphInteractiveBackend(ClingraphBackend):
    """
    ClingraphInteractiveBackend class.
    """

    def __init__(self, args):
        super().__init__(args)

        self._options_encoding_files = args.options_encoding
        self._intermediate_format = "svg"
        self._graphs = None

    @classmethod
    def register_options(cls, parser):
        """
        Register specific arguments.
        """

        ClingraphBackend.register_options(parser)

        parser.add_argument(
            "--options-encoding",
            help="Encoding for the options, must return facts of type option_context/5",
            nargs=1,
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
        super(ClingraphBackend, self)._update_uifb_ui()
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


