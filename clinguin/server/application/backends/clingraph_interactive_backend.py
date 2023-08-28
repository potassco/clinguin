# pylint: disable=R0801,C0103,E1123,R0912,R0915,R1705
"""
Module that packs the clingraph interactive backend.
TODO -> Integrate this functionality to normal clingraph backend.
"""
import textwrap

import clingo
import clingraph
from clorm.clingo import Control as ClormControl

from clinguin.server import ClinguinBackend
from clinguin.server.application.backends import ClingoBackend
from clinguin.server import StandardJsonEncoder

from .standard_utils.clingo_logger import ClingoLogger
from .standard_utils.interactivity_options_contexts import (
    Option_Context,
    OptionsList,
    Select_Option,
    createOptionsList,
)


class ClingraphInteractiveBackend(ClingoBackend):
    """
    ClingraphInteractiveBackend class.
    """

    def __init__(self, args):
        super().__init__(args)

        self._program = args.program[0]
        self._viz_encoding = args.viz_encoding[0]
        self._options_encoding = args.options_encoding[0]
        self._user_input_encoding = args.user_input_encoding[0]

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
                raw = self.graphUpdateHelper("")
                element.attributes.append(raw)

        return json_structure
        
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
            "--program",
            help=textwrap.dedent(
                """\
                            The ASP-program that will be used to create the basic graph."""
            ),
            nargs=1,
        )
        parser.add_argument("--viz-encoding", help="Encoding for clingraph", nargs=1)
        parser.add_argument(
            "--options-encoding",
            help="Encoding for the options, must return facts of type option_context/5",
            nargs=1,
        )
        parser.add_argument(
            "--user-input-encoding",
            help="Optional encoding file in case there is need for seperation between regular program and "
            "usage of user_input/5",
            nargs=1,
        )

    def graphUpdate(self, *kwargs):
        if self._uifb.is_empty:
            self._update_uifb()
        self._logger.debug(self._uifb)
        json_structure = StandardJsonEncoder.encode(self._uifb)

        looked_upon_elements = [json_structure]
        while len(looked_upon_elements) > 0:
            element = looked_upon_elements.pop(0)
            looked_upon_elements = looked_upon_elements + element.children

            if element.type == "clingraph_interactive":
                raw = self.graphUpdateHelper(*kwargs)
                element.attributes.append(raw)

        return json_structure

    def graphUpdateHelper(self, *kwargs):
        """
        Updates the graph and returns it.
        """

        """
        for arg in kwargs:
            print(arg)
        """

        try:
            ctl = clingo.Control(logger=ClingoLogger.logger)
            ctl.load(self._program)

            if kwargs[0] != "":
                input_prg = ".\n".join(kwargs) + "."
                ctl.add(input_prg)
                ctl.load(self._user_input_encoding)

            ctl.ground()
            models = []
            with ctl.solve(yield_=True) as handle:
                for model in handle:
                    symbols = model.symbols(atoms=True, terms=True)
                    models.append([str(symbol) for symbol in symbols])

            if len(models) <= 0:
                if len(input_prg) > 0:
                    return Exception(
                        "There are no solutions to your program with this user input!"
                    )
                else:
                    return Exception("There are no solutions to your program!")
        except RuntimeError as e:
            return Exception(
                "An error occurred while solving/grounding your program and user input: "
                + str(e)
                + "\n"
                + "Particular: "
                + ClingoLogger.errorString()
            )

        model_string = ".\n".join(models[0]) + "."
        try:
            ctl = clingo.Control(logger=ClingoLogger.logger)
            ctl.add(model_string)
            ctl.load(self._viz_encoding)
            ctl.ground(context=clingraph.clingo_utils.ClingraphContext())
            fb = clingraph.Factbase()
            with ctl.solve(yield_=True) as handle:
                for model in handle:
                    fb.add_model(model)
                    break
        except RuntimeError as e:
            return Exception(
                "An error occured during the Clingraph stage: "
                + str(e)
                + " Particular: "
                + ClingoLogger.errorString()
            )

        if len(fb.get_facts()) <= 0:
            return Exception(
                "Your program and your clingraph encoding do not return a model,"
                + "(or do not return one that can be used by clingraph)"
            )

        options_models = []
        try:
            clorm_ctl = ClormControl(
                unifier=[Option_Context, Select_Option], logger=ClingoLogger.logger
            )
            clorm_ctl.add(model_string)
            clorm_ctl.load(self._options_encoding)
            clorm_ctl.ground()
            with clorm_ctl.solve(yield_=True) as handle:
                for model in handle:
                    facts = model.facts(atoms=True, terms=True)
                    options_models.append(facts)
                    break

            if len(options_models) <= 0:
                return Exception(
                    "Could not solve your options encoding with your program output. No options will be displayed"
                )
        except RuntimeError as e:
            return Exception(
                "An error occured during the Option solving stage: "
                + str(e)
                + " Particular: "
                + ClingoLogger.errorString()
            )

        options_list: OptionsList = createOptionsList(options_models[0])
        graph = clingraph.compute_graphs(fb)
        clingraph.render(graph, format="svg")
        with open("out/default.svg", "r", encoding="UTF-8") as svg_file:
            svg_content = svg_file.read()

        raw = {"key":"clingraph_interactive", "value":"", "data": svg_content, "option_data": options_list.to_json()}
        return raw
