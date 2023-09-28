# pylint: disable=R0801
"""
Module that contains the ClingoMultishotBackend.
"""
import base64
import os
from pathlib import Path

from clingo import Control, parse_term
from clingo.script import enable_python
from clingo.symbol import Function, String
from clorm import Raw

from clinguin.server import UIFB, ClinguinBackend, StandardJsonEncoder
from clinguin.server.data.attribute import AttributeDao
from clinguin.utils import StandardTextProcessing

enable_python()


class ClingoBackend(ClinguinBackend):
    """
    The Single-shot Backend class is a backend that is reduced to the most important functionality.
    It only contains policies for adding and removing atoms and will reground after each user input.
    """

    def __init__(self, args):
        super().__init__(args)

        self._domain_files = args.domain_files
        self._ui_files = args.ui_files
        self._constants = [f"-c {v}" for v in args.const] if args.const else []

        self._init_setup()
        self._end_browsing()
        self._init_ctl()
        self._ground()

        include_unsat_msg = not args.ignore_unsat_msg
        self._uifb = UIFB(
            self._ui_files,
            self._constants,
            include_menu_bar=args.include_menu_bar,
            include_unsat_msg=include_unsat_msg,
        )

        self._encoding = "utf-8"
        self._attribute_image_key = "image"

    # ---------------------------------------------
    # Required methods
    # ---------------------------------------------

    def get(self, force_update=False):
        """
        Overwritten default method to get the gui as a Json structure.
        """
        if force_update or self._uifb.is_empty:
            self._update_uifb()
        self._logger.debug(self._uifb)
        json_structure = StandardJsonEncoder.encode(self._uifb)
        return json_structure

    @classmethod
    def register_options(cls, parser):
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

    # ---------------------------------------------
    # Private methods
    # ---------------------------------------------

    def _init_setup(self):
        """
        Initial setup of properties
        """
        # For browising
        self._handler = None
        self._iterator = None

        # To make static linters happy
        self._atoms = set()
        self._ctl = None

    def _init_ctl(self):
        self._ctl = Control(["0"] + self._constants)

        existant_file_counter = 0
        for f in self._domain_files:
            path = Path(f)
            if path.is_file():
                try:
                    self._ctl.load(str(f))
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
                "None of the provided domain files exists or they can't be parsed by clingo. At least one syntactically"
                + "valid domain file must be specified."
            )
            self._logger.critical(exception_string)
            raise Exception(exception_string)

        for atom in self._atoms:
            self._ctl.add("base", [], str(atom) + ".")

    def _ground(self):
        self._ctl.ground([("base", [])])

    def _end_browsing(self):
        if self._handler:
            self._handler.cancel()
            self._handler = None
        self._iterator = None

    @property
    def _is_browsing(self):
        return self._iterator is not None

    @property
    def _backend_state_prg(self):
        """
        Additional program to pass to the UI computation. It represents to the state of the backend
        """
        state_prg = "#defined _clinguin_browsing/0. #defined _clinguin_context/2. "
        if self._is_browsing:
            state_prg += "_clinguin_browsing."
        if self._uifb.is_unsat:
            state_prg += "_clinguin_unsat."
        for a in self.context:
            value = str(a.value)
            try:
                symbol = parse_term(value)
            except:
                symbol = None
            if symbol is None:
                value = f'"{value}"'
            state_prg += f"_clinguin_context({str(a.key)},{value})."
        return state_prg

    @property
    def _output_prg(self):
        """
        Output program used when downloading into file
        """
        prg = ""
        for a in self._atoms:
            prg = prg + f"{str(a)}.\n"
        return prg


    def _update_uifb_consequences(self):
        self._uifb.update_all_consequences(self._ctl, self._assumptions)
        if self._uifb.is_unsat:
            self._logger.error(
                "domain files are UNSAT. Setting _clinguin_unsat to true"
            )

    def _update_uifb_ui(self):
        self._uifb.update_ui(self._backend_state_prg)

        self._replace_uifb_with_b64_images()

    def _update_uifb(self):
        self._update_uifb_consequences()
        self._update_uifb_ui()

    def _set_auto_conseq(self, model):
        self._uifb.set_auto_conseq(model)

    def _solve_set_handler(self):
        self._handler = self._ctl.solve(yield_=True)

    def _add_atom(self, predicate_symbol):
        if predicate_symbol not in self._atoms:
            self._atoms.add(predicate_symbol)
    # ---------------------------------------------
    # Policies
    # ---------------------------------------------

    def restart(self):
        """
        Policy: Restart 
        """
        self._init_setup()
        self._end_browsing()
        self._init_ctl()
        self._ground()
        self._update_uifb()
    def download(self, show_prg= None, file_name = "clinguin_download.lp"):
        """
        Policy: Downloads the current state of the backend. All added atoms and assumptions
        are put together as a list of facts. 

        Args:
            show_prg (_type_, optional): Program to filter output using show statements. Defaults to None.
            file_name (str, optional): The name of the file for the download. Defaults to "clinguin_download.lp".

        """
        prg = self._output_prg
        was_browsing = self._is_browsing
        self._end_browsing()
        self._update_uifb()
        if was_browsing:
            self._uifb.add_message("Warning", "Browsing was active during download, only selected solutions will be present on the file.", "warning")
        if show_prg is not None:
            ctl = Control()
            ctl.add("base", [], prg)
            ctl.add("base", [], show_prg.replace('"',''))
            ctl.ground([("base", [])])
            with ctl.solve(yield_=True) as hnd:
                for m in hnd:
                    atoms = [f"{str(s)}." for s in m.symbols(shown=True)]
            
            prg = "\n".join(atoms)

        
        with open(file_name, "w") as file:
            file.write(prg)
        self._uifb.add_message("Download successful", f"Information saved in file {file_name}.", "success")
        


    def clear_atoms(self):
        """
        Policy: clear_atoms removes all atoms, then basically ''resets'' the backend (i.e. it regrounds, etc.)
        and finally updates the model and returns the updated gui as a Json structure.
        """
        self._end_browsing()
        self._atoms = set()
        self._init_ctl()
        self._ground()

        self._update_uifb()
    def add_atom(self, predicate):
        """
        Policy: Adds an assumption and basically resets the rest of the application (reground) -
        finally it returns the udpated Json structure.
        """
        predicate_symbol = parse_term(predicate)
        if predicate_symbol not in self._atoms:
            self._add_atom(predicate_symbol)
            self._init_ctl()
            self._ground()
            self._end_browsing()
            self._update_uifb()
    def remove_atom(self, predicate):
        """
        Policy: Removes an assumption and basically resets the rest of the application (reground) -
        finally it returns the udpated Json structure.
        """
        predicate_symbol = parse_term(predicate)
        if predicate_symbol in self._atoms:
            self._atoms.remove(predicate_symbol)
            self._init_ctl()
            self._ground()
            self._end_browsing()
            self._update_uifb()

    def next_solution(self, opt_mode="ignore"):
        """
        Policy: Obtains the next solution
        Arguments:
            opt_mode: The clingo optimization mode, bu default is 'ignore', to browse only optimal models use 'optN'
        """
        if self._ctl.configuration.solve.opt_mode != opt_mode:
            self._logger.debug("Ended browsing since opt mode changed")
            self._end_browsing()
        optimizing = opt_mode in ["optN", "opt"]
        if not self._iterator:
            self._ctl.configuration.solve.enum_mode = "auto"
            self._ctl.configuration.solve.opt_mode = opt_mode
            self._ctl.configuration.solve.models = 0
            self._solve_set_handler()
            self._iterator = iter(self._handler)
        try:
            model = next(self._iterator)
            while optimizing and not model.optimality_proven:
                self._logger.info("Skipping non-optimal model")
                model = next(self._iterator)
            self._set_auto_conseq(model)
            self._update_uifb_ui()
        except StopIteration:
            self._logger.info("No more solutions")
            self._end_browsing()
            self._update_uifb()
            self._uifb.add_message("Browsing Information", "No more solutions")

    def select(self):
        """
        Policy: Select the current solution during browsing
        """
        self._end_browsing()
        last_model_symbols = self._uifb.get_auto_conseq()
        for s in last_model_symbols:  # pylint: disable=E1133
            self._add_atom(s)
        self._update_uifb()
    def _replace_uifb_with_b64_images(self):
        attributes = list(self._uifb.get_attributes())
        for attribute in attributes:
            if str(attribute.key) != self._attribute_image_key:
                continue

            attribute_value = StandardTextProcessing.parse_string_with_quotes(
                str(attribute.value)
            )

            if os.path.isfile(attribute_value):
                with open(attribute_value, "rb") as image_file:
                    encoded_string = self._image_to_b64(image_file.read())
                    new_attribute = AttributeDao(
                        Raw(Function(str(attribute.id), [])),
                        Raw(Function(str(attribute.key), [])),
                        Raw(String(str(encoded_string))),
                    )
                    self._uifb.replace_attribute(attribute, new_attribute)

    def _image_to_b64(self, img):
        encoded = base64.b64encode(img)
        decoded = encoded.decode(self._encoding)
        return decoded
