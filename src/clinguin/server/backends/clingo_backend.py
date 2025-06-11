# pylint: disable=R0801
# pylint: disable=too-many-lines
"""
Module that contains the ClingoBackend.
"""
from argparse import ArgumentParser
from types import SimpleNamespace

import logging
import time
import os
from pathlib import Path
from typing import List, Dict, Set, Optional, Tuple, Any
from dataclasses import dataclass, field, fields

from clingo import Control, parse_term
from clingo.script import enable_python

from clinguin.server.ui import UIState

from clinguin.server.domain_state import DomainState

from clinguin.utils.logging import domctl_log
from clinguin.server.json_encoder import JsonEncoder

# from ....utils.transformer import UsesSignatureTransformer

enable_python()
# pylint: disable=attribute-defined-outside-init
log = logging.getLogger(__name__)

# class ClinguinFile():
#     """
#     A class to represent a Clinguin file.

#     Attributes:
#         path (str): The path to the file.
#         content (str): The content of the file.
#     """

#     def __init__(self, path: str, content: str):
#         self.path = path
#         self.content = content

#     def __repr__(self):
#         return f"ClinguinFile(path={self.path}, content={self.content})"


@dataclass
class BackendArgs:
    """Base arguments for ClingoBackend."""

    VALID_OPT_MODES = {"opt", "enum", "optN", "ignore"}

    domain_files: List[str] = field(default_factory=list)
    ui_files: List[str] = field(default_factory=list)
    const: List[str] = field(default_factory=list)
    clingo_ctl_arg: List[str] = field(default_factory=list)
    default_opt_mode: str = "ignore"
    opt_timeout: Optional[int] = None

    def __post_init__(self):
        """Validates that file paths exist and are actual files."""
        for file_path in self.domain_files + self.ui_files:
            if not os.path.isfile(file_path):
                raise ValueError(f"Invalid file path: {file_path} does not exist or is not a file.")

        # Validate `default_opt_mode`
        if self.default_opt_mode not in self.VALID_OPT_MODES:
            valid_options = ", ".join(self.VALID_OPT_MODES)
            raise ValueError(
                f"Invalid default_opt_mode: '{self.default_opt_mode}'. " f"Must be one of: {valid_options}"
            )

        for c in self.const:
            values = c.split("=")
            if (len(values) != 2) or (not values[0]) or (not values[1]):
                raise ValueError("Invalid constant format. Expected name=value.")

    @classmethod
    def from_args(cls, args: SimpleNamespace):
        """Creates BackendArgs from `args`, filtering out extra fields."""
        valid_fields = {f.name for f in fields(cls)}  # Get valid field names
        filtered_args = {k: v for k, v in vars(args).items() if k in valid_fields}  # Keep only valid fields
        return cls(**filtered_args)

    @classmethod
    def register_options(cls, parser: ArgumentParser):
        """Registers CLI options dynamically based on BackendArgs fields."""
        defaults = cls()  # Create a BackendArgs instance to get default values

        parser.add_argument(
            "--domain-files",
            nargs="+",
            help="Files with the domain-specific encodings.",
            default=defaults.domain_files,
            metavar="",
        )
        parser.add_argument(
            "--ui-files", nargs="+", help="Files defining the UI encodings.", default=defaults.ui_files, metavar=""
        )
        parser.add_argument(
            "-c",
            "--const",
            action="append",
            help="Constant passed to Clingo, e.g., <id>=<term>.",
            default=defaults.const,
            metavar="",
        )
        parser.add_argument(
            "--clingo-ctl-arg",
            action="append",
            help="Arguments passed to the Clingo control object.",
            default=defaults.clingo_ctl_arg,
            metavar="",
        )
        parser.add_argument(
            "--default-opt-mode",
            type=str,
            help="Default optimization mode.",
            default=defaults.default_opt_mode,
            metavar="",
        )
        parser.add_argument(
            "--opt-timeout",
            type=int,
            help="Optional timeout for optimization.",
            default=defaults.opt_timeout,
            metavar="",
        )


class ClingoBackend:
    """
    This backend contains the basic clingo functionality for a backend using clingo.

      Attributes:
        _args (BackendArgs): Arguments for the backend.
        _ds_constructor (DomainState): DomainState constructor to generate the domain state.

        _constants (dict[str, str]): Constants that might be set interactively.
        _context (list): Stores the context during interactions.
        _ctl (Optional[clingo.Control]): Clingo control object for solving `domain-ctl`.
        _ui_state (Optional[UIState]): UIState object managing UI construction.
        _atoms (set[str]): Set of dynamically defined atoms.
        _assumptions (set[tuple[str, bool]]): Set of assumptions (atom, boolean).
        _externals (dict[str, set[str]]): External atoms (true, false, released).
        _handler (Optional[clingo.SolveHandle]): Solve handle for browsing.
        _iterator (Optional[Iterator]): Iterator for browsing solutions.
        _model (Optional[list[clingo.Symbol]]): Stores the current model.
        _unsat_core (Optional[list[int]]): Stores the unsatisfiable core. Its presence indicates an UNSAT result.
        _cost (list): Cost values assigned to the current model by optimization.
        _optimal (bool): Whether the solution is optimal.
        _optimizing (bool): Whether the request asked for optimal models.
        _messages (list[tuple[str, str, str]]): Messages sent to the UI. Include warning, errors and information.

        _domain_state_constructors (list[str]): List of domain state constructors (methods to generate the domain state).
    """

    args_class = BackendArgs
    ds_class = DomainState

    # Set on the initialization
    _context: List[Any]
    _ctl: Optional[Any]
    _ui_state: Optional[Any]  # UIState class
    _atoms: Set[str]
    _assumptions: Set[Tuple[str, bool]]
    _externals: Dict[str, Set[str]]
    _constants: Dict[str, str]
    _handler: Optional[Any]  # clingo.SolveHandle
    _iterator: Optional[Any]
    _model: Optional[List[Any]]  # clingo.Symbol
    _unsat_core: Optional[List[int]]
    _cost: List[Any]
    _optimal: bool
    _optimizing: bool
    _messages: List[Tuple[str, str, str]]

    _domain_state_constructors: List[str]

    def __init__(self, args: BackendArgs):
        """
        Creates the clingo backend with the given arguments.
        It will setup all attributes by calling :func:`~_restart()`.

        Generally this method should NOT be overwritten by custom backends.
        Instead, custom backends should overwrite specialized methods.

        Arguments:
            args (BackendArgs): The arguments for the backend. When using it in the CLI these are the arguments registered in :func:`~register_options`.

        """
        self._args = args
        self._ds_constructor = self.ds_class(self)

        # Restart the backend to initialize all internal attributes
        self._restart()

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
    def _constants_argument_list(self) -> List[str]:
        """
        Gets the constants as a list of strings in the format "-c <name>=<value>"
        """
        return [f"-c {k}={v}" for k, v in self._constants.items()]

    @property
    def _ctl_arguments_list(self) -> list[str]:
        """
        Gets the list of arguments used for creating a control object
        """
        return ["0"] + self._constants_argument_list + [f"--{o}" for o in self._args.clingo_ctl_arg]

    @property
    def _assumption_list(self) -> set[tuple[str, bool]]:
        """
        A list of assumptions in the format of form (a, True) or (a, False)
        """
        return self._assumptions

    # ---------------------------------------------
    # Initialization
    # ---------------------------------------------

    def _restart(self):
        """
        Restarts the backend by setting all attributes,
        initializing controls and grounding.
        It is automatically called when the server starts.

        See Also:
            :func:`~_init_command_line`, :func:`~_init_interactive`,
            :func:`~_outdate`, :func:`~_init_ctl`, :func:`~_ground`
        """
        self._init_command_line()
        self._init_interactive()
        self._outdate()
        self._init_ctl()
        self._ground()

    def _init_command_line(self):
        """
        Initializes the attributes based on the provided arguments.
        It is the place to do any post-processing of the arguments.
        This method is called when the server starts or after a restart.

        Sets:
            _constants (dict[str, str]): Dictionary of constants passed via `-c name=value`.

        Example:

            .. code-block:: python

                    def _init_command_line(self):
                        super()._init_command_line()
                        self._my_custom_attr = self._args.my_custom_option


        Raises:
            ValueError: If a constant is provided in an invalid format.
        """

        self._constants = {}
        if self._args.const is not None:
            for c in self._args.const:
                name, value = c.split("=")
                self._constants[name] = value

    def _init_interactive(self):
        """
        Initializes the attributes that will change during the interaction.
        This method is called when the server starts or after a restart.

        Sets:
            _context (list): A list to store the context set by the general handler of requests.
            _ctl (Optional[clingo.Control]): The domain control set in `_init_ctl`.
            _ui_state (Optional[UIState]): A UIState object used to handle the UI construction,
            _atoms (set[str]): Stores dynamically set atoms.
            _assumptions (set[tuple[str, bool]]): Assumptions made during interaction.
            _externals (dict[str, set[str]]): External atoms set interactively categorized as true, false, or released.
            _handler (Optional[clingo.SolveHandle]): Solve handle when browsing.
            _iterator (Optional[Iterator]): Iterator for browsing solutions.
            _model (Optional[list[clingo.Symbol]]): Stores the last found model.
            _unsat_core (Optional[list[int]]): Stores the unsatisfiable core.
            _cost (list): Cost values assigned to the current model.
            _optimal (bool): Whether the current solution is optimal.
            _optimizing (bool): Whether the solver is optimizing.
            _messages (list[tuple[str, str, str]]): Messages to be displayed in the UI.
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

        See Also:
            :func:`~_create_ctl`, :func:`~_load_and_add`
        """
        self._create_ctl()
        self._load_and_add()

    def _create_ctl(self) -> None:
        """
        Initializes the control object (domain-control).
        It is used when the server is started or after a restart.

        See Also:
            :func:`~_load_file`
        """
        log.debug(domctl_log(f"domainctl = Control({self._ctl_arguments_list})"))
        self._ctl = Control(self._ctl_arguments_list)

    def _load_and_add(self) -> None:
        """
        Loads domain files and atoms into the control.

        This method iterates over the domain files and atoms specified in the instance and loads them into the control.
        It raises an exception if a domain file does not exist or if there is a syntax error in the logic program file.

        Raises:
            Exception: If a domain file does not exist or if there is a syntax error in the logic program file.

        See Also:
            :func:`~_load_file`
        """
        for f in self._args.domain_files:
            path = Path(f)
            if not path.is_file():
                log.critical("File %s does not exist", f)
                raise FileNotFoundError(f"File {f} does not exist")

            try:
                self._load_file(f)
            except Exception as e:
                log.critical(
                    "Failed to load file %s (there is likely a syntax error in this logic program file).",
                    f,
                )
                log.critical(str(e))
                raise e

        for atom in self._atoms:
            log.debug(domctl_log('domctl.add("base", [], {str(atom)} + ".")'))
            self._ctl.add("base", [], str(atom) + ".")

    def _load_file(self, f):
        """
        Loads a file into the control. This method can be overwritten if any pre-processing is needed.

        Arguments:
            f (str): The file path
        """
        log.debug(domctl_log(f"domctl.load({str(f)})"))
        self._ctl.load(str(f))

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
        self._ds_constructor.clear_cache()

    # ---------------------------------------------
    # Setters
    # ---------------------------------------------

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

        Args:
            name (str): name of the constant
            value (Any): value of the constant
        """
        name = name.strip('"')
        self._constants[name] = value
        value = str(value).strip('"')
        self._constants[name] = value
        log.debug("Constant %s updated successfully to %s", name, value)

    def _add_atom(self, predicate_symbol):
        """
        Adds an atom if it hasn't been already added

        Arguments:
            predicate_symbol (clingo.Symbool): The symbol for the atom
        """
        if predicate_symbol not in self._atoms:
            self._atoms.add(predicate_symbol)

    def _set_external(self, symbol, name):
        """
        Sets the external value of a symbol.

        Args:
            symbol (clingo.Symbol): The clingo symbol to be set
            name (str): Either "true", "false" or "release"
        """
        name = name.strip('"')
        if name == "release":
            log.debug(domctl_log(f"ctl.release_external({symbol})"))
            self._ctl.release_external(symbol)
            self._externals["released"].add(symbol)

            if symbol in self._externals["true"]:
                self._externals["true"].remove(symbol)

            if symbol in self._externals["false"]:
                self._externals["false"].remove(symbol)

        elif name == "true":
            log.debug(domctl_log(f"ctl.assign_external({symbol}, True)"))
            self._ctl.assign_external(symbol, True)
            self._externals["true"].add(symbol)

            if symbol in self._externals["false"]:
                self._externals["false"].remove(symbol)

        elif name == "false":
            log.debug(domctl_log(f"ctl.assign_external({symbol}, False)"))
            self._ctl.assign_external(symbol, False)
            self._externals["false"].add(symbol)

            if symbol in self._externals["true"]:
                self._externals["true"].remove(symbol)

        else:
            raise ValueError(f"Invalid external value {name}. Must be true, false or relase")

    def _add_assumption(self, symbol, value="true"):
        """
        Adds an assumption to the list of assumptions.

        Args:
            symbol (clingo.Symbol): The clingo symbol to be added as a True assumption
            value (true): The value of the assumption either "true" or "false"
        """
        bool_val = value == "true"
        self._assumptions.add((symbol, bool_val))

    # ---------------------------------------------
    # Solving
    # ---------------------------------------------

    def _ground(self, program="base", arguments=None):
        """
        Grounds the provided program

        Arguments:
            program (str): The name of the program to ground (defaults to "base")
            arguments (list, optional): The list of arguments to ground the program. Defaults to an empty list.
        """
        arguments = arguments or []
        arguments = [arguments] if not isinstance(arguments, list) else arguments
        log.debug(domctl_log(f"domctl.ground([({program}, {arguments})])"))
        arguments_symbols = [parse_term(a) for a in arguments]
        self._ctl.ground([(program, arguments_symbols)])

    def _prepare(self):
        """
        Does any preparation before a solve call.
        """

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
            log.debug("       Cost: %s", model.cost)
        self._optimal = model.optimality_proven
        self._cost = model.cost

    # ---------------------------------------------
    # UI state
    # ---------------------------------------------

    def _update_ui_state(self):
        """
        Updates the UI state by calling all domain state methods
        and creating a new control object (ui_control) using the UI files provided
        """
        domain_state = self._ds_constructor.get_domain_state()
        self._ui_state = UIState(self._args.ui_files, domain_state, self._constants_argument_list)
        self._ui_state.update_ui_state()
        self._ui_state.replace_images_with_b64()
        for m in self._messages:
            self._ui_state.add_message(m[0], m[1], m[2])
        self._messages = []

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
        return JsonEncoder.encode(self._ui_state, self._ds_constructor.get_domain_state_dict())

    def restart(self):
        """
        Restarts the backend. It will initialize all attributes, remove atoms, assumptions and externals,
        restart the control object by initializing all parameters, controls, ending the browsing and grounding.
        """
        self._restart()

    def ground(self, program, arguments=None):
        """
        Grounds the given program. Notice that the base program is grounded when the server starts.
        This operation can be used for grounding encodings with multiple programs in a multi-shot setting.

        Arguments:
            program (str): The name of the program to ground used in the #program directive
            arguments (tuple, optional): The list of arguments to ground the program. Defaults to an empty list.
            These are the arguments of your #program directive. For instance, in #program step(t). the argument is t.
        """
        self._ground(program, arguments)

    def update(self):
        """
        Updates the UI by clearing the cache and computing the models again.
        """
        self._ds_constructor.clear_cache()

    def download(self, show_prg=None, file_name="clinguin_download.lp"):
        """
        Downloads the current model. It must be selected first via :func:`~select` .

        Arguments:
            show_prg (_type_, optional): Program to filter output using show statements. Defaults to None.
            file_name (str, optional): The name of the file for the download. Defaults to "clinguin_download.lp".
        """
        if self._model is None:
            raise RuntimeError("Cant download when there is no model")
        show_prg = show_prg or ""
        prg = "\n".join([f"{s}." for s in self._model])
        ctl = Control()
        ctl.add("base", [], prg)
        try:
            ctl.add("base", [], show_prg.replace('"', ""))
        except RuntimeError as exc:
            raise Exception("Show program can't be parsed. Make sure it is a valid clingo program.") from exc
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
        Removes all atoms and resets the backend.
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
        otherwise it iterates the models in the last call. To keep the atoms shown in the solution, use :func:`~select`.

        Arguments:
            opt_mode: The clingo optimization mode, bu default is 'ignore', to browse only optimal models use 'optN'
        """
        if self._ctl.configuration.solve.opt_mode != opt_mode:
            log.debug("Ended browsing since opt mode changed")
            self._outdate()
        optimizing = opt_mode in ["optN", "opt"]
        if not self._iterator:
            log.debug(domctl_log(f"domctl.configuration.solve.opt_mode = {opt_mode}"))
            self._ctl.configuration.solve.enum_mode = "auto"
            self._ctl.configuration.solve.opt_mode = opt_mode
            self._ctl.configuration.solve.models = 0

            self._prepare()
            log.debug(domctl_log(f"domctl.solve({[(str(a),b) for a,b in self._assumption_list]}, yield_=True)"))
            self._handler = self._ctl.solve(self._assumption_list, yield_=True)

            self._iterator = iter(self._handler)
        try:
            start = time.time()
            model = next(self._iterator)
            self._ds_constructor.clear_cache(["_ds_model"])
            self._on_model(model)
            self._model = model.symbols(shown=True, atoms=True, theory=True)
            while optimizing and not model.optimality_proven:
                if len(model.cost) == 0:
                    self._messages.append(
                        (
                            "Browsing Warning",
                            "No optimization provided",
                            "warning",
                        )
                    )
                    log.warning(
                        "No optimization statement provided in encoding but optimization condition provided\
                            in 'next_solution' operation. Exiting browsing."
                    )
                    break
                if self._args.opt_timeout is not None and time.time() - start > self._args.opt_timeout:
                    log.warning(
                        "Timeout for finding optimal model was reached. Returning model without proving optimality."
                    )
                    break
                log.debug("Skipping non-optimal model!")
                model = next(self._iterator)
                self._ds_constructor.clear_cache(["_ds_model"])
                self._on_model(model)

            self._model = model.symbols(shown=True, atoms=True, theory=True)
        except StopIteration:
            print(
                "optimizing",
            )
            print(optimizing)
            if optimizing:
                m = "No more optimal solutions"
            else:
                m = "No more solutions"

            log.info(m)
            self._outdate()
            self._messages.append(("Browsing Information", m, "info"))

    def clear_assumptions(self):
        """
        Removes all assumptions.
        """
        # pylint: disable=attribute-defined-outside-init
        self._outdate()
        self._assumptions = set()

    def add_assumption(self, atom, value="true"):
        """
        Adds an atom `a` as an assumption.

        If the value is "true", the atom is assumed to be true.
        This assumption can be considered as an integrity constraint:
        ``:- not a.`` forcing the program to entail the given atom.

        If the value is "false", the atom is assumed to be false:
        This assumption can be considered as an integrity constraint:
        ``:- a.`` forcing the program to never entail the given atom.

        Notice that the assumption must be generated by your domain encoding.

        Arguments:

            atom (str): The clingo symbol to be added as a true assumption
            value (str): The value of the assumption either "true" or "false"
        """
        atom_symbol = parse_term(atom)
        if atom_symbol not in [a[0] for a in self._assumptions]:
            self._add_assumption(atom_symbol, value)
            self._outdate()

    def remove_assumption(self, atom):
        """
        Removes an atom from the assumptions list regardless of its value.
        This will allow the atom to take any value in the solution.

        Arguments:
            atom (str): The clingo symbol to be removed
        """
        atom_symbol = parse_term(atom)
        for a, v in self._assumptions:
            if a == atom_symbol:
                self._assumptions.remove((a, v))
                self._outdate()
                return

    def remove_assumption_signature(self, atom):
        """
        Removes from the list of assumptions those matching the given atom.
        Unlike function remove_assumption, this one allows for partial matches using the
        placeholder constant `any`.
        This will allow the atom to take any value in the solution.

        Arguments:

            atom (str): The atom description as a symbol,
                where the reserver word `any` is used to state that anything can
                take part of that position. For instance, `person(anna,any)`,
                will remove all assumptions of atom person, where the first argument is anna.
        """
        atom_symbol = parse_term(atom)
        arity = len(atom_symbol.arguments)
        to_remove = []
        for s, v in self._assumptions:
            if s.match(atom_symbol.name, arity):
                for i, a in enumerate(atom_symbol.arguments):
                    if str(a) != "any" and s.arguments[i] != a:
                        break
                else:
                    to_remove.append((s, v))
                    continue
        for a in to_remove:
            self._assumptions.remove(a)
        if len(to_remove) > 0:
            self._outdate()

    def set_external(self, atom, value):
        """
        Sets the value of an external. Externals must be defined in the domain files using `#external`.
        The truth value of external atoms can then be provided by the user via this function.

        Arguments:

            atom (str): The clingo symbol to be set
            value (str): The value (release, true or false)
        """
        symbol = parse_term(atom)
        name = value
        self._outdate()

        self._set_external(symbol, name)

    def select(self, show_prg: str = ""):
        """
        Select the current solution during browsing.
        All atoms in the solution are added as assumptions in the backend.

        Arguments:

            show_program (str): An optional show program to filter atoms

        """
        if self._model is None:
            self._messages.append(("No solution", "There is no solution to be selected", "danger"))
            log.error("No solution. No model has been computed that can be selected")
        else:
            symbols_to_ignore = self._externals["true"]
            symbols_to_ignore.union(self._externals["false"])
            if show_prg == "":
                model = self._model
            else:
                model = []
                ctl = Control(["--warn=none"])
                try:
                    ctl.add("base", [], show_prg.strip('"'))
                except RuntimeError as exc:
                    raise Exception("Show program can't be parsed. Make sure it is a valid clingo program.") from exc
                prg = "\n".join([f"{str(s)}." for s in self._model])
                ctl.add("base", [], prg)
                ctl.ground([("base", [])])

                def add_shown(m):
                    for s in m.symbols(shown=True):
                        model.append(s)

                ctl.solve(on_model=add_shown)
            for s in model:  # pylint: disable=E1133
                if s not in symbols_to_ignore:
                    self._add_assumption(s, "true")
        self._outdate()

    def stop_browsing(self):
        """
        Stops the current browsing.
        """
        self._outdate()

    def set_constant(self, name: str, value: Any):
        """
        Sets a constant value. Will reinitialize the control, ground and set arguments
        """
        self._set_constant(name, value)
        self._init_interactive()
        self._outdate()
        self._init_ctl()
        self._ground()
