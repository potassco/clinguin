# pylint: disable=R0801
"""
Module that contains the ClingoMultishotBackend.
"""
import os
from pathlib import Path

from clingo import Control, parse_term
from clingo.script import enable_python
from clingo.symbol import Function, String
from clorm import Raw

from clinguin.server import UIFB, ClinguinBackend, StandardJsonEncoder
from clinguin.server.data.attribute import AttributeDao
from clinguin.utils import StandardTextProcessing, image_to_b64
enable_python()


class ClingoBackend(ClinguinBackend):
    """
    The ClingoBackend contains the basic clingo functionality for grounding and solving.

    When started it sets up all the arguments provided via the command line,
    and creates a control object (domain-control) with the provided domain files.
    It grounds the program and creates an empty UI state.
    """

    def __init__(self, args):
        super().__init__(args)

        self._domain_files = [] if args.domain_files is None else args.domain_files
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
            include_unsat_msg=include_unsat_msg,
        )

        self._encoding = "utf-8"
        self._attribute_image_key = "image"

    # ---------------------------------------------
    # Required methods
    # ---------------------------------------------

    def get(self):
        """
        Updates the UI and transforms the facts into a JSON.
        This method will be automatically called after executing all the operations.
        Thus, it needs to be implemented by all backends.

        The UI is only updated if there are any changes.
        """
        if self._uifb.is_empty:
            self._update_uifb()
        self._logger.debug(self._uifb)
        json_structure = StandardJsonEncoder.encode(self._uifb)
        return json_structure

    @classmethod
    def register_options(cls, parser):
        """
        Registers options in the command line for the domain files and ui files.
        """
        parser.add_argument("--domain-files", nargs="+", help="Files with the domain specific encodings and the instances", metavar="")
        parser.add_argument(
            "--ui-files", nargs="+", help="Files with the encodings that generate the UI predicates: elem, attr and when", metavar=""
        )
        parser.add_argument(
            "-c",
            "--const",
            nargs="+",
            help="Constant passed to clingo, <id>=<term> replaces term occurrences of <id> with <term>",
            metavar="",
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
        Initializes the arguments when the server starts or after a restart. 
        These arguments include, the handler and intetor for browsing answer sets, as well as the domain control and the atoms.,
        """
        # For browising
        self._handler = None
        self._iterator = None

        # To make static linters happy
        self._atoms = set()
        self._ctl = None

    def _init_ctl(self):
        """
        Initializes the control object (domain-control). 
        It is used when the server is started or after a restart.
        Uses the provided constants and domain files.
        It adds the atoms.
        """
        self._ctl = Control(["0"] + self._constants)

        existant_file_counter = 0
        for f in self._domain_files:
            path = Path(f)
            if path.is_file():
                try:
                    self._ctl.load(str(f))
                    existant_file_counter += 1
                except Exception(exception_string):
                    self._logger.critical(
                        "Failed to load file %s (there is likely a syntax error in this logic program file).",
                        f,
                    )
                    self._logger.critical(exception_string)
                    raise Exception(exception_string)

            else:
                self._logger.critical(
                    "File %s does not exist", f
                )        
                raise Exception("File %s does not exist", f)

        for atom in self._atoms:
            self._ctl.add("base", [], str(atom) + ".")

    def _ground(self, program="base"):
        """
        Grounds the provided program

        Args:
            program (str): The name of the program to ground (defaults to "base")
        """
        self._ctl.ground([(program, [])])

    def _end_browsing(self):
        """
        Any current interation in the models wil be terminated by canceling the search and removing the iterator
        """
        if self._handler:
            self._handler.cancel()
            self._handler = None
        self._iterator = None

    @property
    def _is_browsing(self):
        """
        Checks if clinguin is in browsing mode.
        """
        return self._iterator is not None

    @property
    def _clinguin_state(self):
        """
        Creates the atoms that will be part of the clinguin state, which is passed to the UI computation.
        
        Includes predicates  _clinguin_browsing/0 and _clinguin_context/2
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
        Generates the output program used when downloading into a file
        """
        prg = ""
        for a in self._atoms:
            prg = prg + f"{str(a)}.\n"
        return prg

    def _on_model(self, model):
        """
        This method is called each time a model is obtained by the domain control.
        It can be used to extend the given model in Theory Solving.

        Args:
            model (clingo.Model): The found clingo model
        """
        pass

    def _update_uifb_consequences(self):
        """
        Updates the brave and cautious consequences of the domain state.
        """
        self._uifb.update_all_consequences(self._ctl, [], self._on_model)
        if self._uifb.is_unsat:
            self._logger.error(
                "Domain files are UNSAT. Setting _clinguin_unsat to true"
            )

    def _update_uifb_ui(self):
        """
        Updates the ui state with the previously computed domain state.
        Any image is replaced by a b64 representation
        """
        self._uifb.update_ui(self._clinguin_state)

        self._replace_uifb_with_b64_images()

    def _update_uifb(self):
        """
        Updates the domain-state (brave and cautious consequences) and the ui-state
        """
        self._update_uifb_consequences()
        self._update_uifb_ui()

    def _set_auto_conseq(self, model):
        """
        Sets the given model in the domain-state

        Args:
            model (clingo.Model): The model found by the solving
        """
        self._uifb.set_auto_conseq(model)

    def _solve_set_handler(self):
        """
        Sets the solveng handler by calling the solve method of clingo
        """
        self._handler = self._ctl.solve(yield_=True)

    def _add_atom(self, predicate_symbol):
        """
        Adds an atom if it hasn't been already aded

        Args:
            predicate_symbol (clingo.Symbool): The symbol for the atom
        """
        if predicate_symbol not in self._atoms:
            self._atoms.add(predicate_symbol)

    def _replace_uifb_with_b64_images(self):
        """
        Replaces all images in the ui-state by b64
        """
        attributes = list(self._uifb.get_attributes())
        for attribute in attributes:
            if str(attribute.key) != self._attribute_image_key:
                continue

            attribute_value = StandardTextProcessing.parse_string_with_quotes(
                str(attribute.value)
            )

            if os.path.isfile(attribute_value):
                with open(attribute_value, "rb") as image_file:
                    encoded_string = image_to_b64(image_file.read())
                    new_attribute = AttributeDao(
                        Raw(Function(str(attribute.id), [])),
                        Raw(Function(str(attribute.key), [])),
                        Raw(String(str(encoded_string))),
                    )
                    self._uifb.replace_attribute(attribute, new_attribute)


    # ---------------------------------------------
    # Policies
    # ---------------------------------------------

    def restart(self):
        """
        Restarts the backend by initializing parameters, controls, ending the browsing grounding and updating the UI
        """
        self._init_setup()
        self._end_browsing()
        self._init_ctl()
        self._ground()
        self._update_uifb()

    def update(self):
        """
        Updates the UI and transforms the output into a JSON.
        """
        self._update_uifb()
    
    def download(self, show_prg= None, file_name = "clinguin_download.lp", domain_files = True):
        """
        Downloads the current state of the backend. All added atoms and assumptions
        are put together as a list of facts. 

        Args:
            show_prg (_type_, optional): Program to filter output using show statements. Defaults to None.
            file_name (str, optional): The name of the file for the download. Defaults to "clinguin_download.lp".
            domain_files (bool, optional): If the domain files should be included. Defaults to True

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
            if domain_files:
                for f in self._domain_files:
                    ctl.load(f)
            ctl.add("base", [], show_prg.replace('"',''))
            ctl.ground([("base", [])])
            with ctl.solve(yield_=True) as hnd:
                for m in hnd:
                    atoms = [f"{str(s)}." for s in m.symbols(shown=True)]
            
            prg = "\n".join(atoms)

        file_name = file_name.strip('"')
        with open(file_name, "w") as file:
            file.write(prg)
        self._uifb.add_message("Download successful", f"Information saved in file {file_name}.", "success")
        


    def clear_atoms(self):
        """
        Removes all atoms and resets the backend (i.e. it regrounds, etc.)
        and finally updates the model and returns the updated gui as a Json structure.
        """
        self._end_browsing()
        self._atoms = set()
        self._init_ctl()
        self._ground()

        self._update_uifb()
    
    def add_atom(self, predicate):
        """
        Adds an assumption, restarts the control and grounds again
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
        Removes an assumption, restarts the control and grounds again
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
        Obtains the next solution. If a no browsing has been started yet, then it calls solve,
        otherwise it iterates the models in the last call.
        
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
        Select the current solution during browsing. All atoms in the solution are added as atoms in the backend.
        """
        self._end_browsing()
        last_model_symbols = self._uifb.get_auto_conseq()
        for s in last_model_symbols:  # pylint: disable=E1133
            self._add_atom(s)
        self._update_uifb()
    