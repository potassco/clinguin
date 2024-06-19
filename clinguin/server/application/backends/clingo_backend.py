# pylint: disable=R0801
"""
Module that contains the ClingoMultishotBackend.
"""
import logging
from functools import cached_property
from pathlib import Path
import functools

from clingo import Control, parse_term
from clingo.script import enable_python

from clinguin.server import StandardJsonEncoder, UIState
from clinguin.server.data.domain_state import solve, tag

from ....utils.logger import domctl_log
from ....utils.transformer import UsesSignatureTransformer

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
        if not args.ui_files:
            raise RuntimeError("UI files need to be provided under --ui-files")
        self._ui_files = args.ui_files
        self._constants = args.const if args.const else []
        self._clingo_ctl_arg = args.clingo_ctl_arg if args.clingo_ctl_arg else []

        self._domain_state_constructors = []
        self._backup_ds_cache = {}

        self._init_setup()
        self._outdate()
        self._init_ctl()
        self._ground()

        self._add_domain_state_constructor("_ds_context")
        self._add_domain_state_constructor("_ds_opt")
        self._add_domain_state_constructor("_ds_unsat")
        self._add_domain_state_constructor("_ds_browsing")
        self._add_domain_state_constructor("_ds_cautious_optimal")
        self._add_domain_state_constructor("_ds_brave_optimal")
        self._add_domain_state_constructor("_ds_cautious")
        self._add_domain_state_constructor("_ds_brave")
        self._add_domain_state_constructor("_ds_model")  # Keep after brave and cautious

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
            action="append",
            help="Constant passed to clingo, <id>=<term> replaces term occurrences of <id> with <term>",
            metavar="",
        )
        parser.add_argument(
            "--clingo-ctl-arg",
            action="append",
            help="""Argument that will be passed to clingo control object for the domain.
            Should have format <name>=<value>, for example parallel-mode=2 will become --parallel-mode=2.""",
            metavar="",
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

        self._cost = []  # Set in on_model
        self._optimal = False  # Set in on_model
        self._optimizing = False  # Set in on_model

    def _init_ctl(self):
        """
        Creates the control and loads the files
        """
        self._create_ctl()
        self._load_and_add()

    @property
    def _ctl_arguments_list(self):
        """
        Gets the list of arguments used for creating a control object
        """
        return (
            ["0"]
            + [f"-c {v}" for v in self._constants]
            + [f"--{o}" for o in self._clingo_ctl_arg]
        )

    def _create_ctl(self):
        """
        Initializes the control object (domain-control).
        It is used when the server is started or after a restart.
        """
        self._ctl = Control(self._ctl_arguments_list)
        self._logger.debug(
            domctl_log(f"domain_ctl = Control({self._ctl_arguments_list})")
        )

    def _load_and_add(self):
        """
        Loads domain files and atoms into the control
        """
        for f in self._domain_files:
            path = Path(f)
            if not path.is_file():
                self._logger.critical("File %s does not exist", f)
                raise Exception(f"File {f} does not exist")

            try:
                self._load_file(f)
            except Exception as e:
                self._logger.critical(
                    "Failed to load file %s (there is likely a syntax error in this logic program file).",
                    f,
                )
                self._logger.critical(str(e))
                raise e

        for atom in self._atoms:
            self._ctl.add("base", [], str(atom) + ".")
            self._logger.debug(domctl_log('domctl.add("base", [], {str(atom)} + ".")'))

    def _load_file(self, f):
        """
        Loads a file into the control. This method can be overwritten if any pre-processing is needed.

        Arguments:
            f (str): The file path
        """
        self._ctl.load(str(f))
        self._logger.debug(domctl_log(f"domctl.load({str(f)})"))

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
        self._logger.debug(domctl_log(f"domctl.ground([({program}, [])])"))

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
        self._optimizing = len(model.cost) > 0
        self._optimal = model.optimality_proven
        self._cost = model.cost

    def _add_atom(self, predicate_symbol):
        """
        Adds an atom if it hasn't been already aded

        Arguments:
            predicate_symbol (clingo.Symbool): The symbol for the atom
        """
        if predicate_symbol not in self._atoms:
            self._atoms.add(predicate_symbol)

    def _get_assumptions(self):
        """
        Gets the set of assumptions used for solving
        """
        return self._assumptions

    # ---------------------------------------------
    # UI update
    # ---------------------------------------------

    def _update_ui_state(self):
        """
        Updates the UI state by calling all domain state methods
        and creating a new control object (ui_control) using the ui_files provided
        """
        domain_state = self._domain_state
        self._ui_state = UIState(self._ui_files, domain_state, self._constants)
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

    def _call_solver_with_cache(self, ds_id: str):
        """
        Generic function to call the using exiting cache on browsing

        Arguments:
            ds_id: Identifier used in the cache
        Returns:
            A list of symbols
        """
        if self._is_browsing:
            return (
                self._backup_ds_cache[ds_id] if ds_id in self._backup_ds_cache else ""
            )
        self._prepare()
        symbols, ucore = solve(
            self._ctl, [(a, True) for a in self._get_assumptions()], self._on_model
        )
        self._logger.debug(
            domctl_log(
                f"domctl.solve(assumptions={[(str(a), True) for a in self._get_assumptions()]}, yield_=True)"
            )
        )
        self._unsat_core = ucore
        if symbols is None:
            self._logger.warning("Got an UNSAT result with the given domain encoding.")
            return (
                self._backup_ds_cache[ds_id] if ds_id in self._backup_ds_cache else ""
            )
        return symbols

    @functools.lru_cache(maxsize=None)
    def _ui_uses_predicate(self, name: str, arity: int):
        """
        Returns a truth value of weather the ui_files contain the given signature.

        Args:
            name (str): Predicate name
            arity (int): Predicate arity
        """
        transformer = UsesSignatureTransformer(name, arity)
        self._logger.debug(f"Transformer parsing UI files to find {name}/{arity}")
        transformer.parse_files(self._ui_files)
        return transformer.contained

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
        prg = "#defined _clinguin_context/2. "
        for a in self.context:
            value = str(a.value)
            try:
                symbol = parse_term(value)
            except Exception:
                symbol = None
            if symbol is None:
                value = f'"{value}"'
            prg += f"_clinguin_context({str(a.key)},{value})."
        return prg + "\n"

    @cached_property
    def _ds_brave(self):
        """
        Computes brave consequences adds them as predicates ``_any/1``.

        It uses a cache that is erased after an operation makes changes in the control.
        """
        if not self._ui_uses_predicate("_any", 1):
            return ""

        self._ctl.configuration.solve.models = 0
        self._ctl.configuration.solve.opt_mode = "ignore"
        self._ctl.configuration.solve.enum_mode = "brave"
        self._logger.debug(domctl_log('domctl.configuration.solve.enum_mode = "brave"'))
        symbols = self._call_solver_with_cache("_ds_brave")
        return " ".join([str(s) + "." for s in list(tag(symbols, "_any"))]) + "\n"

    @cached_property
    def _ds_cautious(self):
        """
        Computes cautious consequences adds them as predicates ``_all/1``.

        It uses a cache that is erased after an operation makes changes in the control.
        """
        if not self._ui_uses_predicate("_all", 1):
            return ""

        self._ctl.configuration.solve.models = 0
        self._ctl.configuration.solve.opt_mode = "ignore"
        self._ctl.configuration.solve.enum_mode = "cautious"
        self._logger.debug(
            domctl_log('domctl.configuration.solve.enum_mode = "cautious"')
        )
        symbols = self._call_solver_with_cache("_ds_cautious")
        return " ".join([str(s) + "." for s in list(tag(symbols, "_all"))]) + "\n"

    @cached_property
    def _ds_model(self):
        """
        Computes model

        It uses a cache that is erased after an operation makes changes in the control.
        """
        self._ctl.configuration.solve.models = 0
        self._ctl.configuration.solve.opt_mode = "ignore"
        self._ctl.configuration.solve.enum_mode = "auto"
        self._logger.debug(domctl_log('domctl.configuration.solve.enum_mode = "auto"'))
        symbols = self._call_solver_with_cache("_ds_model")
        return " ".join([str(s) + "." for s in symbols]) + "\n"

    @cached_property
    def _ds_brave_optimal(self):
        """
        Computes brave consequences for only optimal solutions adds them as predicates ``_any_opt/1``.

        It uses a cache that is erased after an operation makes changes in the control.
        """
        if not self._ui_uses_predicate("_any_opt", 1):
            return ""

        self._ctl.configuration.solve.models = 0
        self._ctl.configuration.solve.opt_mode = "optN"
        self._ctl.configuration.solve.enum_mode = "brave"
        self._logger.debug(domctl_log('domctl.configuration.solve.opt_mode = "optN"'))
        self._logger.debug(domctl_log('domctl.configuration.solve.enum_mode = "brave"'))
        symbols = self._call_solver_with_cache("_ds_brave_optimal")
        return " ".join([str(s) + "." for s in list(tag(symbols, "_any_opt"))]) + "\n"

    @cached_property
    def _ds_cautious_optimal(self):
        """
        Computes cautious consequences adds them as predicates ``_all_opt/1``.

        It uses a cache that is erased after an operation makes changes in the control.
        """
        if not self._ui_uses_predicate("_all_opt", 1):
            return ""

        self._ctl.configuration.solve.models = 0
        self._ctl.configuration.solve.opt_mode = "optN"
        self._ctl.configuration.solve.enum_mode = "cautious"
        self._logger.debug(domctl_log('domctl.configuration.solve.opt_mode = "optN"'))
        self._logger.debug(
            domctl_log('domctl.configuration.solve.enum_mode = "cautious"')
        )
        symbols = self._call_solver_with_cache("_ds_cautious_optimal")
        return " ".join([str(s) + "." for s in list(tag(symbols, "_all_opt"))]) + "\n"

    @property
    def _ds_unsat(self):
        """
        Adds information about the statisfiablity of the domain control

        Includes predicate ``_clinguin_unsat/0`` if the domain control is unsat
        """
        prg = "#defined _clinguin_unsat/0. "
        if self._unsat_core is not None:
            prg += "_clinguin_unsat."
        return prg + "\n"

    @property
    def _ds_browsing(self):
        """
        Adds information about the browsing state

        Includes predicate  ``_clinguin_browsing/0`` if the user is browsing solutions
        """
        prg = "#defined _clinguin_browsing/0. "
        if self._is_browsing:
            prg += "_clinguin_browsing."
        return prg + "\n"

    @property
    def _ds_opt(self):
        """
        Additional program to pass to the UI with optimality info
        """
        prg = "#defined _clinguin_cost/2.\n#defined _clinguin_cost/1.\n#defined _clinguin_optimal/1.\n"
        prg += f"_clinguin_cost({tuple(self._cost)}).\n"

        for i, c in enumerate(self._cost):
            prg += f"_clinguin_cost({i},{c}).\n"
        if self._optimal:
            prg += "_clinguin_optimal.\n"
        if self._optimizing:
            prg += "_clinguin_optimizing.\n"
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

    def download(self, show_prg=None, file_name="clinguin_download.lp"):
        """
        Downloads the current model.

        Arguments:
            show_prg (_type_, optional): Program to filter output using show statements. Defaults to None.
            file_name (str, optional): The name of the file for the download. Defaults to "clinguin_download.lp".
        """
        if self._model is None:
            raise RuntimeError("Cant download when there is no model")
        prg = "\n".join([f"{s}." for s in self._model])
        ctl = Control()
        ctl.add("base", [], prg)
        try:
            ctl.add("base", [], show_prg.replace('"', ""))
        except RuntimeError as exc:
            raise Exception(
                "Show program can't be parsed. Make sure it is a valid clingo program."
            ) from exc
        ctl.ground([("base", [])])
        with ctl.solve(yield_=True) as hnd:
            for m in hnd:
                atoms = [f"{str(s)}." for s in m.symbols(shown=True)]

        final_prg = "\n".join(atoms)

        file_name = file_name.strip('"')
        with open(file_name, "w", encoding="UTF-8") as file:
            file.write(final_prg)
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
            self._logger.debug(
                domctl_log(f"domctlconfiguration.solve.opt_mode = {opt_mode}")
            )

            self._prepare()
            self._handler = self._ctl.solve(
                [(a, True) for a in self._get_assumptions()], yield_=True
            )
            self._logger.debug(
                domctl_log(
                    f"domctlsolve({[(a, True) for a in self._get_assumptions()]}, yield_=True)"
                )
            )

            self._iterator = iter(self._handler)
        try:
            model = next(self._iterator)
            while optimizing and not model.optimality_proven:
                self._logger.info("Skipping non-optimal model!")
                model = next(self._iterator)
            self._clear_cache(["_ds_model"])
            self._on_model(model)
            self._model = model.symbols(shown=True, atoms=True, theory=True)
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

    def stop_browsing(self):
        """
        Stops the current browsing
        """
        self._outdate()
