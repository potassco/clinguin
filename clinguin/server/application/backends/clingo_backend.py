# pylint: disable=R0801
"""
Module that contains the ClingoMultishotBackend.
"""
import logging
from functools import cached_property
from pathlib import Path

from clingo import Control, parse_term
from clingo.script import enable_python

from clinguin.server import StandardJsonEncoder, UIState
from clinguin.server.data.domain_state import solve, tag

enable_python()
# pylint: disable=attribute-defined-outside-init


class ClingoBackend:
    """
    The ClingoBackend contains the basic clingo functionality for a backend using clingo.

    When started it sets up all the arguments provided via the command line,
    and creates a control object (domain-control) with the provided domain files.
    It grounds the program and creates an empty UI state.
    """

    def __init__(self, args):
        """
        Creates the Backend with the given arguments. It will setup the context, files and constants.
        It will define all domain-state constructors and their cache.
        Finally, it calls all the setup methods: (_init_setup, _outdate,_init_ctl) and grounds the control

        Arguments:
            args (ArgumentParser): The arguments from the argument parser that are given for the registered options.
        """
        self._logger = logging.getLogger(args.log_args["name"])
        self.context = []
        self.args = args

        self._domain_files = [] if args.domain_files is None else args.domain_files
        self._ui_files = args.ui_files
        self._constants = [f"-c {v}" for v in args.const] if args.const else []
        self._include_unsat_msg = not args.ignore_unsat_msg

        self._domain_state_constructors = []
        self._backup_ds_cache = {}

        self._init_setup()
        self._outdate()
        self._init_ctl()
        self._ground()

        self._add_domain_state_constructor("_ds_context")
        self._add_domain_state_constructor("_ds_brave")
        self._add_domain_state_constructor("_ds_cautious")
        self._add_domain_state_constructor("_ds_model")
        self._add_domain_state_constructor("_ds_unsat")
        self._add_domain_state_constructor("_ds_browsing")

    # ---------------------------------------------
    # Class methods
    # ---------------------------------------------

    @classmethod
    def register_options(cls, parser):
        """
        Registers options in the command line for the domain files and ui files.

        Arguments:
            parser (ArgumentParser): A group of the argparse argument parser
        """
        parser.add_argument(
            "--domain-files",
            nargs="+",
            help="Files with the domain specific encodings and the instances",
            metavar="",
        )
        parser.add_argument(
            "--ui-files",
            nargs="+",
            help="Files with the encodings that generate the UI predicates: elem, attr and when",
            metavar="",
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
    # Context
    # ---------------------------------------------

    def _set_context(self, context):
        """
        Sets the context

        Arguments:
            context: The context dictionary
        """
        self.context = context

    # ---------------------------------------------
    # Setups
    # ---------------------------------------------

    def _init_setup(self):
        """
        Initializes the arguments when the server starts or after a restart.
        These arguments include, the handler and iterator for browsing answer sets,
        as well as the domain control and the atoms.
        """
        # For browising
        self._handler = None
        self._iterator = None

        # To make static linters happy
        self._atoms = set()
        self._ctl = None

        self._model = None
        self._assumptions = set()
        self._unsat_core = None

        self._ui_state = None
        self._messages = []

    def _init_ctl(self):
        """
        Initializes the control object (domain-control).
        It is used when the server is started or after a restart.
        Uses the provided constants and domain files.
        It adds the atoms.
        """
        self._ctl = Control(["0"] + self._constants)

        for f in self._domain_files:
            path = Path(f)
            if not path.is_file():
                self._logger.critical("File %s does not exist", f)
                raise Exception(f"File {f} does not exist")

            try:
                self._ctl.load(str(f))
            except Exception as e:
                self._logger.critical(
                    "Failed to load file %s (there is likely a syntax error in this logic program file).",
                    f,
                )
                self._logger.critical(str(e))
                raise e

        for atom in self._atoms:
            self._ctl.add("base", [], str(atom) + ".")

    def _outdate(self):
        """
        Outdates all the dynamic values when a change has been made.
        Any current interaction in the models wil be terminated by canceling the search and removing the iterator.
        """
        if self._handler:
            self._handler.cancel()
            self._handler = None
        self._iterator = None
        self._model = None
        self._clear_cache()

    @property
    def _is_browsing(self):
        """
        Property to tell if clinguin is in browsing mode.
        """
        return self._iterator is not None

    # ---------------------------------------------
    # Solving
    # ---------------------------------------------

    def _ground(self, program="base"):
        """
        Grounds the provided program

        Arguments:
            program (str): The name of the program to ground (defaults to "base")
        """
        self._ctl.ground([(program, [])])

    def _prepare(self):
        """
        Does any preparation before a solve call.
        """

    def _on_model(self, model):
        """
        This method is called each time a model is obtained by the domain control.
        It can be used to extend the given model in Theory Solving.

        Arguments:
            model (clingo.Model): The found clingo model
        """

    def _add_atom(self, predicate_symbol):
        """
        Adds an atom if it hasn't been already aded

        Arguments:
            predicate_symbol (clingo.Symbool): The symbol for the atom
        """
        if predicate_symbol not in self._atoms:
            self._atoms.add(predicate_symbol)

    # ---------------------------------------------
    # UI update
    # ---------------------------------------------

    def _update_ui_state(self):
        """
        Updates the UI state by calling all domain state methods
        and creating a new control object (ui_control) using the ui_files provided
        """
        domain_state = self._domain_state
        self._ui_state = UIState(
            self._ui_files, domain_state, self._constants, self._include_unsat_msg
        )
        self._ui_state.update_ui_state()
        self._ui_state.replace_images_with_b64()
        for m in self._messages:
            self._ui_state.add_message(m[0], m[1], m[2])
        self._messages = []

    # ---------------------------------------------
    # Domain state
    # ---------------------------------------------

    def _add_domain_state_constructor(self, method: str):
        """
        Adds a method name to the domain constructors.
        This method needs to be annotated with ``@property`` or ``@cached_property``

        Arguments:
            method (str): Name of the property method
        """

        self._domain_state_constructors.append(method)

    def _clear_cache(self, methods=None):
        """
        Clears the cache of domain state constructor methods

        Arguments:
            methods (list, optional): A list with the methods to remove the cache from.
                If no value is passed then all cache is removed
        """
        if methods is None:
            methods = self._domain_state_constructors
        for m in methods:
            if m in self.__dict__:
                self._backup_ds_cache[m] = self.__dict__[m]
                del self.__dict__[m]

    @property
    def _domain_state(self):
        """
        Gets the domain state by calling all the domain constructor methods
        """
        ds = ""
        for f in self._domain_state_constructors:
            ds += getattr(self, f)
        return ds

    # -------- Domain state methods

    @property
    def _ds_context(self):
        """
        Gets the context as facts ``_clinguin_context(KEY, VALUE)``
        """
        prg = ""
        for a in self.context:
            value = str(a.value)
            try:
                symbol = parse_term(value)
            except Exception:
                symbol = None
            if symbol is None:
                value = f'"{value}"'
            prg += f"_clinguin_context({str(a.key)},{value})."
        return prg

    @cached_property
    def _ds_brave(self):
        """
        Computes brave consequences adds them as predicates ``_any/1``.

        It uses a cache that is erased after an operation makes changes in the control.
        """
        if self._is_browsing:
            return (
                self._backup_ds_cache["_ds_brave"]
                if "_ds_brave" in self._backup_ds_cache
                else ""
            )
        self._ctl.configuration.solve.models = 0
        self._ctl.configuration.solve.opt_mode = "ignore"
        self._ctl.configuration.solve.enum_mode = "brave"
        self._prepare()
        symbols, ucore = solve(
            self._ctl, [(a, True) for a in self._assumptions], self._on_model
        )
        self._unsat_core = ucore
        if symbols is None:
            self._logger.warning("Got an UNSAT result with the given domain encoding.")
            return (
                self._backup_ds_cache["_ds_brave"]
                if "_ds_brave" in self._backup_ds_cache
                else ""
            )
        return "\n".join([str(s) + "." for s in list(tag(symbols, "_any"))])

    @cached_property
    def _ds_cautious(self):
        """
        Computes cautious consequences adds them as predicates ``_all/1``.

        It uses a cache that is erased after an operation makes changes in the control.
        """
        if self._is_browsing:
            return (
                self._backup_ds_cache["_ds_cautious"]
                if "_ds_cautious" in self._backup_ds_cache
                else ""
            )
        self._ctl.configuration.solve.models = 0
        self._ctl.configuration.solve.opt_mode = "ignore"
        self._ctl.configuration.solve.enum_mode = "cautious"
        self._prepare()
        symbols, ucore = solve(
            self._ctl, [(a, True) for a in self._assumptions], self._on_model
        )
        self._unsat_core = ucore
        if symbols is None:
            self._logger.warning("Got an UNSAT result with the given domain encoding.")
            return (
                self._backup_ds_cache["_ds_cautious"]
                if "_ds_cautious" in self._backup_ds_cache
                else ""
            )
        return "\n".join([str(s) + "." for s in list(tag(symbols, "_all"))])

    @cached_property
    def _ds_model(self):
        """
        Computes a model if one has not been set yet.
        When the model is being iterated by the user, the current model is returned.
        It uses a cache that is erased after an operation makes changes in the control.
        """
        if self._model is None:
            self._ctl.configuration.solve.models = 1
            self._ctl.configuration.solve.opt_mode = "ignore"
            self._ctl.configuration.solve.enum_mode = "auto"
            self._prepare()
            symbols, ucore = solve(
                self._ctl, [(a, True) for a in self._assumptions], self._on_model
            )
            self._unsat_core = ucore
            if symbols is None:
                self._logger.warning(
                    "Got an UNSAT result with the given domain encoding."
                )
                return (
                    self._backup_ds_cache["_ds_model"]
                    if "_ds_model" in self._backup_ds_cache
                    else ""
                )
            self._model = symbols

        return "\n".join([str(s) + "." for s in self._model])

    @property
    def _ds_unsat(self):
        """
        Adds information about the statisfiablity of the domain control

        Includes predicate ``_clinguin_unsat/0`` if the domain control is unsat
        """
        prg = "#defined _clinguin_unsat/0."
        if self._unsat_core:
            prg += "_clinguin_unsat."
        return prg

    @property
    def _ds_browsing(self):
        """
        Adds information about the browsing state

        Includes predicate  ``_clinguin_browsing/0`` if the user is browsing solutions
        """
        prg = "#defined _clinguin_browsing/0."
        if self._is_browsing:
            prg += "_clinguin_browsing."
        return prg

    # ---------------------------------------------
    # Output
    # ---------------------------------------------

    @property
    def _output_prg(self):
        """
        Generates the output program used when downloading into a file
        """
        prg = ""
        for a in self._atoms:
            prg = prg + f"{str(a)}.\n"
        return prg

    ########################################################################################################

    # ---------------------------------------------
    # Public operations
    # ---------------------------------------------

    def get(self):
        """
        Updates the UI and transforms the facts into a JSON.
        This method will be automatically called after executing all the operations.
        Thus, it needs to be implemented by all backends.
        """
        self._update_ui_state()
        self._logger.debug(self._ui_state)
        json_structure = StandardJsonEncoder.encode(self._ui_state)
        return json_structure

    def restart(self):
        """
        Restarts the backend by initializing parameters, controls, ending the browsing grounding and updating the UI
        """
        self._init_setup()
        self._outdate()
        self._init_ctl()
        self._ground()

    def update(self):
        """
        Updates the UI and transforms the output into a JSON.
        """
        self._clear_cache()

    def download(
        self, show_prg=None, file_name="clinguin_download.lp", domain_files=True
    ):
        """
        Downloads the current state of the backend. All added atoms and assumptions
        are put together as a list of facts.

        Arguments:
            show_prg (_type_, optional): Program to filter output using show statements. Defaults to None.
            file_name (str, optional): The name of the file for the download. Defaults to "clinguin_download.lp".
            domain_files (bool, optional): If the domain files should be included. Defaults to True

        """
        prg = self._output_prg
        was_browsing = self._is_browsing
        self._outdate()
        if was_browsing:
            self._messages.append(
                (
                    "Warning",
                    "Browsing was active during download, only selected solutions will be present on the file.",
                    "warning",
                )
            )
        if show_prg is not None:
            ctl = Control()
            ctl.add("base", [], prg)
            if domain_files:
                for f in self._domain_files:
                    ctl.load(f)
            ctl.add("base", [], show_prg.replace('"', ""))
            ctl.ground([("base", [])])
            with ctl.solve(yield_=True) as hnd:
                for m in hnd:
                    atoms = [f"{str(s)}." for s in m.symbols(shown=True)]

            prg = "\n".join(atoms)

        file_name = file_name.strip('"')
        with open(file_name, "w", encoding="UTF-8") as file:
            file.write(prg)
        self._messages.append(
            (
                "Download successful",
                f"Information saved in file {file_name}.",
                "success",
            )
        )

    def clear_atoms(self):
        """
        Removes all atoms and resets the backend (i.e. it regrounds, etc.)
        and finally updates the model and returns the updated gui as a Json structure.
        """
        self._outdate()
        self._atoms = set()
        self._init_ctl()
        self._ground()

    def add_atom(self, predicate):
        """
        Adds an assumption, restarts the control and grounds again

        Arguments:

            predicate (str): The clingo symbol to be added
        """
        predicate_symbol = parse_term(predicate)
        if predicate_symbol not in self._atoms:
            self._add_atom(predicate_symbol)
            self._init_ctl()
            self._ground()
            self._outdate()

    def remove_atom(self, predicate):
        """
        Removes an assumption, restarts the control and grounds again

        Arguments:

            predicate (str): The clingo symbol to be added
        """
        predicate_symbol = parse_term(predicate)
        if predicate_symbol in self._atoms:
            self._atoms.remove(predicate_symbol)
            self._init_ctl()
            self._ground()
            self._outdate()

    def next_solution(self, opt_mode="ignore"):
        """
        Obtains the next solution. If a no browsing has been started yet, then it calls solve,
        otherwise it iterates the models in the last call.

        Arguments:
            opt_mode: The clingo optimization mode, bu default is 'ignore', to browse only optimal models use 'optN'
        """
        if self._ctl.configuration.solve.opt_mode != opt_mode:
            self._logger.debug("Ended browsing since opt mode changed")
            self._outdate()
        optimizing = opt_mode in ["optN", "opt"]
        if not self._iterator:
            self._ctl.configuration.solve.enum_mode = "auto"
            self._ctl.configuration.solve.opt_mode = opt_mode
            self._ctl.configuration.solve.models = 0
            self._prepare()
            self._handler = self._ctl.solve(
                [(a, True) for a in self._assumptions], yield_=True
            )
            self._iterator = iter(self._handler)
        try:
            model = next(self._iterator)
            while optimizing and not model.optimality_proven:
                self._logger.info("Skipping non-optimal model")
                model = next(self._iterator)
            self._clear_cache(["_ds_model"])
            self._on_model(model)
            self._model = model.symbols(shown=True, atoms=True)
        except StopIteration:
            self._logger.info("No more solutions")
            self._outdate()
            self._messages.append(("Browsing Information", "No more solutions", "info"))

    def select(self):
        """
        Select the current solution during browsing.
        All atoms in the solution are added as atoms in the backend.
        """
        self._outdate()
        if self._model is None:
            self._messages.append(
                "No solution", "There is no solution to be selected", "danger"
            )
        for s in self._model:  # pylint: disable=E1133
            self._add_atom(s)
