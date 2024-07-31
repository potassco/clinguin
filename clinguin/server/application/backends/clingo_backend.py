# pylint: disable=R0801
"""
Module that contains the ClingoMultishotBackend.
"""
import logging
from functools import cached_property
from pathlib import Path
import functools
from typing import Any

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
        Creates the Backend with the given arguments.
        It will setup all attributes by calling :func:`~_init_ds_constructors()` and :func:`~_restart()`.

        Generally this method should NOT be overwritten by custom backends.
        Instead, custom backends should overwrite specialized methods.

        Arguments:
            args (ArgumentParser): The arguments from the argument parser that are given for the registered options.

        """
        self._args = args

        self._logger = logging.getLogger(args.log_args["name"])

        # Setup static attributes that might be changed by custom backends and must be preserved after restarts
        self._init_ds_constructors()

        # Restart the backend to initialize all attributes
        self._restart()

    # ---------------------------------------------
    # Class methods
    # ---------------------------------------------

    @classmethod
    def register_options(cls, parser):
        """
        Registers options in the command line.

        It can be extended by custom backends to add custom command-line options.

        Example:

            .. code-block:: python

                @classmethod
                def register_options(cls, parser):
                    ClingoMultishotBackend.register_options(parser)

                    parser.add_argument(
                        "--my-custom-option",
                        help="Help message",
                        nargs="*",
                    )

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
        parser.add_argument(
            "--default-opt-mode",
            type=str,
            help="Default optimization mode for computing a model",
            default="ignore",
            metavar="",
        )

    # ---------------------------------------------
    # Properties
    # ---------------------------------------------

    @property
    def _is_browsing(self):
        """
        Property to tell if clinguin is in browsing mode.
        """
        return self._iterator is not None

    @property
    def _constants_argument_list(self) -> list:
        """
        Gets the constants as a list of strings in the format "-c <name>=<value>"
        """
        return [f"-c {k}={v}" for k, v in self._constants.items()]

    @property
    def _ctl_arguments_list(self) -> list:
        """
        Gets the list of arguments used for creating a control object
        """
        return (
            ["0"]
            + self._constants_argument_list
            + [f"--{o}" for o in self._clingo_ctl_arg]
        )

    @property
    def _assumption_list(self) -> list:
        """
        A list of assumptions in the format [(a, True)]
        """
        return [(a, True) for a in self._assumptions]

    # ---------------------------------------------
    # Setups
    # ---------------------------------------------

    def _restart(self):
        """
        Restarts the backend by setting all attributes,
        initializing controls and grounding.

        Calls: :func:`~_init_command_line`, :func:`~_init_interactive`, :func:`~_outdate`, :func:`~_init_ctl`, :func:`~_ground`
        """
        self._init_command_line()
        self._init_interactive()
        self._outdate()
        self._init_ctl()
        self._ground()

    def _init_ds_constructors(self):
        """
        This method initializes the domain state constructors list and the backup cache dictionary.
        It also adds the default domain state constructors to the list.
        This method is called only when the server starts.

        Attributes:
            _domain_state_constructors (list): A list to store the domain state constructors.
            _backup_ds_cache (dict): A dictionary to store the backup domain state cache.


        It can be extended by custom backends to add/edit domain state constructors.
        Adding a domain state constructor should be done by calling :func:`~_add_domain_state_constructor()`.

        Example:

            .. code-block:: python

                @property
                def _ds_my_custom_constructor(self):
                    # Creates custom program
                    return "my_custom_program."

                def _init_ds_constructors(self):
                    super()._init_ds_constructors()
                    self._add_domain_state_constructor("_ds_my_custom_constructor")

        """
        self._domain_state_constructors = []
        self._backup_ds_cache = {}
        self._add_domain_state_constructor("_ds_context")
        self._add_domain_state_constructor("_ds_unsat")
        self._add_domain_state_constructor("_ds_browsing")
        self._add_domain_state_constructor("_ds_cautious_optimal")
        self._add_domain_state_constructor("_ds_brave_optimal")
        self._add_domain_state_constructor("_ds_cautious")
        self._add_domain_state_constructor("_ds_brave")
        self._add_domain_state_constructor("_ds_model")  # Keep after brave and cautious
        self._add_domain_state_constructor("_ds_opt")

    def _init_command_line(self):
        """
        Initializes the attributes based on the command-line arguments provided.
        This method is called when the server starts or after a restart.

        Attributes:

            _domain_files (list): The list of domain files provided via command line.
            _ui_files (list): The list of UI files provided via command line.
            _constants (dict): The dictionary of constants provided via command line.
            _clingo_ctl_arg (list): The list of clingo control arguments provided via command line.

        If any command line arguments are added in :func:`~register_options`, they should be initialized here.

        Example:

            .. code-block:: python

                    def _init_command_line(self):
                        super()._init_command_line()
                        self._my_custom_attr = self._args.my_custom_option


        """

        self._domain_files = self._args.domain_files or []

        if not self._args.ui_files:
            raise RuntimeError("UI files need to be provided under --ui-files")
        self._ui_files = self._args.ui_files

        self._constants = {}
        if self._args.const is not None:
            for c in self._args.const:
                if "=" not in c:
                    raise ValueError("Invalid constant format. Expected name=value.")
                name, value = c.split("=")
                self._constants[name] = value

        self._clingo_ctl_arg = self._args.clingo_ctl_arg or []

        self._default_opt_mode = self._args.default_opt_mode

    def _init_interactive(self):
        """
        Initializes the attributes that will change during the interaction.
        This method is called when the server starts or after a restart.

        Attributes:
            _context (list): A list to store the context set by the general handler of requests.
            _handler (clingo.SolveHandle): The handler set while browsing in the `next_solution` operation.
            _iterator (iter): The iterator set while browsing in the `next_solution` operation.
            _ctl (clingo.Control): The domain control set in `_init_ctl`.
            _ui_state (:class:`UIState`): A UIState object used to handle the UI construction, set in every call to `_update_ui_state`.
            _atoms (set[str]): A set to store the atoms set dynamically in operations during the interaction.
            _assumptions (set[str]): A set to store the assumptions set dynamically in operations during the interaction.
            _externals (dict): A dictionary with true, false and released sets of external atoms
            _model (list[clingo.Symbol]): The model set in `on_model`.
            _unsat_core (list[int]): The unsatisfiable core set in `on_model`.
            _cost (list): A list to store the cost set in `on_model`.
            _optimal (bool): A boolean indicating if the solution is optimal, set in `on_model`.
            _optimizing (bool): A boolean indicating if the solver is currently optimizing, set in `on_model`.
            _messages (list[tuple[str,str,str]]): A list to store the messages (title, content, type) to be shown in the UI, set dynamically in operations during the interaction.
        """
        # Context: Set by the general handler of requests
        self._context = []

        # Domain Control: Set in _init_ctl
        self._ctl = None

        # UIState object to handle the UI construction: Set in every time in _update_ui_state
        self._ui_state = None

        # Atoms and assumptions: Set dynamically in operations during the interaction
        self._atoms = set()
        self._assumptions = set()
        self._externals = {"true": set(), "false": set(), "released": set()}

        # Handler and Iterator: Set while browsing in next_solution operation
        self._handler = None
        self._iterator = None

        # Attributes from the model: Set in on_model
        self._model = None
        self._unsat_core = None
        self._cost = []
        self._optimal = False
        self._optimizing = False

        # Messages to be shown in the UI: Set dynamically in operations during the interaction
        self._messages = []

    def _init_ctl(self):
        """
        Creates the domain control and loads the domain files.

        Calls: :func:`~_create_ctl`, :func:`~_load_and_add`
        """
        self._create_ctl()
        self._load_and_add()

    def _create_ctl(self) -> None:
        """
        Initializes the control object (domain-control).
        It is used when the server is started or after a restart.

        Calls: :func:`~_load_file`
        """
        self._logger.debug(
            domctl_log(f"domain_ctl = Control({self._ctl_arguments_list})")
        )
        self._ctl = Control(self._ctl_arguments_list)

    def _load_and_add(self) -> None:
        """
        Loads domain files and atoms into the control.

        This method iterates over the domain files and atoms specified in the instance and loads them into the control.
        It raises an exception if a domain file does not exist or if there is a syntax error in the logic program file.

        Raises:
            Exception: If a domain file does not exist or if there is a syntax error in the logic program file.

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
            self._logger.debug(domctl_log('domctl.add("base", [], {str(atom)} + ".")'))
            self._ctl.add("base", [], str(atom) + ".")

    def _load_file(self, f):
        """
        Loads a file into the control. This method can be overwritten if any pre-processing is needed.

        Arguments:
            f (str): The file path
        """
        self._logger.debug(domctl_log(f"domctl.load({str(f)})"))
        self._ctl.load(str(f))

    def _set_context(self, context):
        """
        Sets the context. Used by general endpoint handler after a request.

        Arguments:
            context: The context dictionary
        """
        self._context = context

    def _set_constant(self, name: str, value: Any) -> None:
        """
        Sets a constant in the backend and restarts the control.

        Calls:  :fun:`~_init_interactive`, :func:`~_outdate`, :func:`~_init_ctl`, :func:`~_ground`

        Args:
            name (str): name of the constant
            value (Any): value of the constant
        """
        self._constants[name] = value
        name = name.strip('"')
        value = str(value).strip('"')
        self._constants[name] = value
        self._logger.debug(f"Constant {name} updated successfully to {value}")
        self._init_interactive()
        self._outdate()
        self._init_ctl()
        self._ground()

    def _outdate(self):
        """
        Outdates all the dynamic values when a change has been made.
        Any current interaction in the models wil be terminated by canceling the search and removing the iterator.

        Calls: :func:`~_clear_cache`
        """
        if self._handler:
            self._handler.cancel()
            self._handler = None
        self._iterator = None
        self._model = None
        self._clear_cache()

    # ---------------------------------------------
    # Solving
    # ---------------------------------------------

    def _ground(self, program="base"):
        """
        Grounds the provided program

        Arguments:
            program (str): The name of the program to ground (defaults to "base")
        """
        self._logger.debug(domctl_log(f"domctl.ground([({program}, [])])"))
        self._ctl.ground([(program, [])])

    def _prepare(self):
        """
        Does any preparation before a solve call.
        """
        pass

    def _on_model(self, model):
        """
        This method is called each time a model is obtained by the domain control.
        It sets the model, and optimization attributes.
        It can be extended to add custom features of the model.

        Arguments:
            model (clingo.Model): The found clingo model
        """
        self._optimizing = len(model.cost) > 0
        if len(model.cost) > 0:
            self._logger.debug("       Cost: %s", model.cost)
        self._optimal = model.optimality_proven
        self._cost = model.cost

    def _add_atom(self, predicate_symbol):
        """
        Adds an atom if it hasn't been already added

        Arguments:
            predicate_symbol (clingo.Symbool): The symbol for the atom
        """
        if predicate_symbol not in self._atoms:
            self._atoms.add(predicate_symbol)

    # ---------------------------------------------
    # UI state
    # ---------------------------------------------

    def _update_ui_state(self):
        """
        Updates the UI state by calling all domain state methods
        and creating a new control object (ui_control) using the UI files provided
        """
        domain_state = self._domain_state
        self._ui_state = UIState(
            self._ui_files, domain_state, self._constants_argument_list
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
        The provided method needs to be annotated with ``@property`` or ``@cached_property``

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

    def _call_solver_with_cache(
        self, ds_id: str, ds_tag: str, models: int, opt_mode: str, enum_mode: str
    ):
        """
        Generic function to call the using exiting cache on browsing.
        Un UNSAT it returns the output saved in the cache

        Arguments:
            ds_id: Identifier used in the cache
        Returns:
            The program tagged
        """
        if self._is_browsing:
            self._logger.debug(f"Returning cache for {ds_id}")
            return (
                self._backup_ds_cache[ds_id] if ds_id in self._backup_ds_cache else ""
            )
        self._logger.debug(domctl_log(f'domctl.configuration.solve.models = {models}"'))
        self._logger.debug(
            domctl_log(f'domctl.configuration.solve.opt_mode = {opt_mode}"')
        )
        self._logger.debug(
            domctl_log(f'domctl.configuration.solve.enum_mode = {enum_mode}"')
        )
        self._ctl.configuration.solve.models = models
        self._ctl.configuration.solve.opt_mode = opt_mode
        self._ctl.configuration.solve.enum_mode = enum_mode
        self._prepare()
        self._logger.debug(
            domctl_log(
                f"domctl.solve({[(str(a),b) for a,b in self._assumption_list]}, yield_=True)"
            )
        )
        symbols, ucore = solve(
            self._ctl,
            self._assumption_list,
            self._on_model,
        )
        self._unsat_core = ucore
        if symbols is None:
            self._logger.warning("Got an UNSAT result with the given domain encoding.")
            return (
                self._backup_ds_cache[ds_id] if ds_id in self._backup_ds_cache else ""
            )
        return " ".join([str(s) + "." for s in list(tag(symbols, ds_tag))]) + "\n"

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
        if not transformer.contained:
            self._logger.debug(
                "Predicate NOT contained. Domain constructor will be skipped"
            )
        return transformer.contained

    @property
    def _domain_state(self):
        """
        Gets the domain state by calling all the domain constructor methods

        Some domain state constructors might skip the computation if the UI does not require them.
        """
        ds = ""
        for f in self._domain_state_constructors:
            ds += f"\n%%%%%%%% {f} %%%%%%%\n"
            ds += getattr(self, f)
        return ds

    # -------- Domain state methods

    @property
    def _ds_context(self):
        """
        Adds context information from the client.

        Includes predicate  ``_clinguin_context/2`` indicating each key and value in the context.
        """
        prg = "#defined _clinguin_context/2. "
        for a in self._context:
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
    def _ds_model(self):
        """
        Computes model and adds all atoms as facts.
        When the model is being iterated by the user, the current model is returned.

        It uses a cache that is erased after an operation makes changes in the control.
        """
        if self._model is None:
            self._logger.debug(
                domctl_log('domctl.configuration.solve.enum_mode = "auto"')
            )
            self._ctl.configuration.solve.models = 1
            self._ctl.configuration.solve.opt_mode = self._default_opt_mode
            self._ctl.configuration.solve.enum_mode = "auto"

            self._prepare()
            self._logger.debug(
                domctl_log(
                    f"domctl.solve({[(str(a),b) for a,b in self._assumption_list]}, yield_=True)"
                )
            )

            symbols, ucore = solve(self._ctl, self._assumption_list, self._on_model)
            self._unsat_core = ucore
            if symbols is None:
                self._logger.warning(
                    "Got an UNSAT result with the given domain encoding."
                )
                return (
                    self._backup_ds_cache["_ds_model"]
                    + "\n".join([str(a) + "." for a in self._atoms])
                    if "_ds_model" in self._backup_ds_cache
                    else ""
                )
            self._model = symbols

        return " ".join([str(s) + "." for s in self._model]) + "\n"

    @cached_property
    def _ds_brave(self):
        """
        Computes brave consequences adds them as predicates ``_any/1``.
        This are atoms that appear in some model.
        If it is not used in the UI files then the computation is not performed.

        It uses a cache that is erased after an operation makes changes in the control.
        """
        if not self._ui_uses_predicate("_any", 1):
            return "% NOT USED\n"

        return self._call_solver_with_cache("_ds_brave", "_any", 0, "ignore", "brave")

    @cached_property
    def _ds_cautious(self):
        """
        Computes cautious consequences adds them as predicates ``_all/1``.
        This are atoms that appear in all models.
        If it is not used in the UI files then the computation is not performed.

        It uses a cache that is erased after an operation makes changes in the control.
        """
        if not self._ui_uses_predicate("_all", 1):
            return "% NOT USED\n"

        return self._call_solver_with_cache(
            "_ds_cautious", "_all", 0, "ignore", "cautious"
        )

    @cached_property
    def _ds_brave_optimal(self):
        """
        Computes brave consequences for only optimal solutions adds them as predicates ``_any_opt/1``.
        This are atoms that appear in some optimal model.
        If it is not used in the UI files then the computation is not performed.

        It uses a cache that is erased after an operation makes changes in the control.
        """
        if not self._ui_uses_predicate("_any_opt", 1):
            return "% NOT USED\n"

        return self._call_solver_with_cache(
            "_ds_brave_optimal", "_any_opt", 0, "optN", "brave"
        )

    @cached_property
    def _ds_cautious_optimal(self):
        """
        Computes cautious consequences of optimal models adds them as predicates ``_all_opt/1``.
        This are atoms that appear in all optimal models.
        If it is not used in the UI files then the computation is not performed.

        It uses a cache that is erased after an operation makes changes in the control.
        """
        if not self._ui_uses_predicate("_all_opt", 1):
            return "% NOT USED\n"

        return self._call_solver_with_cache(
            "_ds_cautious_optimal", "_all_opt", 0, "optN", "cautious"
        )

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
        Adds program to pass with optimality information.

        Includes predicates:
         - ``_clinguin_cost/1``: With a single tuple indicating the cost
         - ``_clinguin_cost/2``: With the index and cost value, linearizing predicate ``_clinguin_cost/1``
         - ``_clinguin_optimal/0``: If the solution is optimal
         - ``_clinguin_optimizing/0``: If there is an optimization in the program
        """
        prg = "#defined _clinguin_cost/2. #defined _clinguin_cost/1. #defined _clinguin_optimal/1. "

        for i, c in enumerate(self._cost):
            prg += f"_clinguin_cost({i},{c}). "
        if self._optimal:
            prg += "_clinguin_optimal. "
        if self._optimizing:
            prg += "_clinguin_optimizing. "

        prg += f"_clinguin_cost({tuple(self._cost)}).\n"
        return prg

    @property
    def _ds_constants(self):
        """
        Adds constants to the domain state.

        Includes predicate ``_clinguin_const/2`` for each constant provided in the command line and used in the domain files
        """
        prg = "#defined _clinguin_const/2. "
        for k, v in self._constants.items():
            prg += f"_clinguin_const({k},{v})."
        return prg + "\n"

    ########################################################################################################

    # ---------------------------------------------
    # Public operations
    # ---------------------------------------------

    def get(self):
        """
        Updates the UI and transforms the facts into a JSON.
        This method will be automatically called after executing all the operations.
        """
        self._update_ui_state()
        json_structure = StandardJsonEncoder.encode(self._ui_state)
        return json_structure

    def restart(self):
        """
        Restarts the backend by initializing all parameters, controls, ending the browsing and grounding
        """
        self._restart()

    def update(self):
        """
        Updates the UI by clearing the cache.
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
        Adds an atom, restarts the control and grounds

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
        Removes an atom (if present), restarts the control and grounds again

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
            self._logger.debug(
                domctl_log(f"domctl.configuration.solve.opt_mode = {opt_mode}")
            )
            self._ctl.configuration.solve.enum_mode = "auto"
            self._ctl.configuration.solve.opt_mode = opt_mode
            self._ctl.configuration.solve.models = 0

            self._prepare()
            self._logger.debug(
                domctl_log(
                    f"domctl.solve({[(str(a),b) for a,b in self._assumption_list]}, yield_=True)"
                )
            )
            self._handler = self._ctl.solve(self._assumption_list, yield_=True)

            self._iterator = iter(self._handler)
        try:
            model = next(self._iterator)
            while optimizing and not model.optimality_proven:
                if len(model.cost) == 0:
                    self._messages.append(
                        (
                            "Browsing Error",
                            "No optimization provided",
                            "error",
                        )
                    )
                    self._logger.error(
                        "No optimization statement provided in encoding but optimization condition provided in 'next_solution' operation. Exiting browsing."
                    )
                    raise StopIteration
                self._logger.debug("Skipping non-optimal model!")
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
        Stops the current browsing.
        """
        self._outdate()

    def set_constant(self, name: str, value: Any):
        """
        Sets a constant value reinitialize the control and grounds
        """
        self._set_constant(name, value)
