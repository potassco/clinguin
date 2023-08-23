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

from .standard_utils.clingo_logger import ClingoLogger
from .standard_utils.interactivity_options_contexts import (
    Option_Context,
    OptionsList,
    Select_Option,
    createOptionsList,
)


class ClingraphInteractiveBackend(ClinguinBackend):
    """
    ClingraphInteractiveBackend class.
    """

    def __init__(self, args):
        super().__init__(args)

        self._program = args.program[0]
        self._viz_encoding = args.viz_encoding[0]
        self._options_encoding = args.options_encoding[0]
        self._user_input_encoding = args.user_input_encoding[0]
        print(args)

    def get(self):
        """
        The get method.
        """
        return self.graphUpdate("")

    @classmethod
    def register_options(cls, parser):
        """
        Register specific arguments.
        """
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
        """
        Updates the graph and returns it.
        """
        for arg in kwargs:
            print(arg)

        try:
            print(self._program)
            ctl = clingo.Control(logger=ClingoLogger.logger)
            ctl.load(self._program)

            if kwargs[0] != "":
                input_prg = ".\n".join(kwargs) + "."
                print("Input prg: ", input_prg)
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
        print(model_string)
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

        print("OPTIONS MODELS: ", options_models[0])
        options_list: OptionsList = createOptionsList(options_models[0])
        graph = clingraph.compute_graphs(fb)
        clingraph.render(graph, format="svg")
        with open("out/default.svg", "r", encoding="UTF-8") as svg_file:
            svg_content = svg_file.read()
        print("Done. Sending response...")
        print("OPTIONSLIST: ", options_list.to_json())
        raw = {"data": svg_content, "option_data": options_list.to_json()}
        return raw
