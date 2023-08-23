# pylint: disable=R0801
"""
Module that contains the ClingoBackend.
"""
from pathlib import Path

from clingo import Control, parse_term
from clingo.script import enable_python

from clinguin.server import UIFB, ClinguinBackend, StandardJsonEncoder

enable_python()


class ClingoBackend(ClinguinBackend):
    """
    The ClingoBackend class is the backend that is selected by default.
    It provides basic functionality to argue bravely and cautiously.
    Further it provides several policies for assumptions, atoms and externals.
    """

    def __init__(self, args):
        super().__init__(args)

        self._domain_files = args.domain_files
        self._ui_files = args.ui_files

        # For browising
        self._handler = None
        self._iterator = None

        # To make static linters happy
        self._assumptions = set()
        self._atoms = set()
        self._ctl = None

        self._end_browsing()
        self._assumptions = set()
        self._externals = {"true": set(), "false": set(), "released": set()}
        self._atoms = set()
        self._constants = [f"-c {v}" for v in args.const] if args.const else []
        self._init_ctl()
        self._ground()

        include_unsat_msg = not args.ignore_unsat_msg
        self._uifb = UIFB(
            self._ui_files,
            self._constants,
            include_menu_bar=args.include_menu_bar,
            include_unsat_msg=include_unsat_msg,
        )

    # ---------------------------------------------
    # Required methods
    # ---------------------------------------------

    def get(self):
        """
        Overwritten default method to get the gui as a Json structure.
        """
        if self._uifb.is_empty:
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
                        'Failed to load file %s (there is likely a syntax error in this logic program file).',
                        f
                    )
            else:
                self._logger.critical(
                    'File %s does not exist, this file is skipped.',
                    f
                )

        if existant_file_counter == 0:
            exception_string = (
                "None of the provided domain files exists, but at least one syntactically"
                + "valid domain file must be specified. Exiting!"
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
        state_prg = "#defined _clinguin_browsing/0. #defined _clinguin_assume/1. "
        if self._is_browsing:
            state_prg += "_clinguin_browsing."
        if self._uifb.is_unsat:
            state_prg += "_clinguin_unsat."
        for a in self._assumptions:
            state_prg += f"_clinguin_assume({str(a)})."
        return state_prg

    def _update_uifb_consequences(self):
        self._uifb.update_all_consequences(self._ctl, self._assumptions)
        if self._uifb.is_unsat:
            self._logger.error(
                "domain files are UNSAT. Setting _clinguin_unsat to true"
            )

    def _update_uifb_ui(self):
        self._uifb.update_ui(self._backend_state_prg)

    def _update_uifb(self):
        self._update_uifb_consequences()
        self._update_uifb_ui()

    def _add_assumption(self, predicate_symbol):
        self._assumptions.add(predicate_symbol)

    # ---------------------------------------------
    # Policies
    # ---------------------------------------------

    def clear_assumptions(self):
        """
        Policy: clear_assumptions removes all assumptions, then basically ''resets'' the backend
        (i.e. it regrounds, etc.) and finally updates the model and returns the updated gui as a Json structure.
        """
        self._end_browsing()
        self._assumptions = set()

        self._update_uifb()
        return self.get()

    def add_assumption(self, predicate):
        """
        Policy: Adds an assumption and returns the udpated Json structure.
        """
        predicate_symbol = parse_term(predicate)
        if predicate_symbol not in self._assumptions:
            self._add_assumption(predicate_symbol)
            self._end_browsing()
            self._update_uifb()
        return self.get()

    def remove_assumption(self, predicate):
        """
        Policy: Removes an assumption and returns the udpated Json structure.
        """
        predicate_symbol = parse_term(predicate)
        if predicate_symbol in self._assumptions:
            self._assumptions.remove(predicate_symbol)
            self._end_browsing()
            self._update_uifb()
        return self.get()

    def remove_assumption_signature(self, predicate):
        """
        Policy: removes predicates with the predicate name of predicate and the given arity
        """
        predicate_symbol = parse_term(predicate)
        arity = len(predicate_symbol.arguments)
        to_remove = []
        for s in self._assumptions:
            if s.match(predicate_symbol.name, arity):
                for i, a in enumerate(predicate_symbol.arguments):
                    if str(a) != "any" and s.arguments[i] != a:
                        break
                else:
                    to_remove.append(s)
                    continue
        for s in to_remove:
            self._assumptions.remove(s)
        if len(to_remove) > 0:
            self._end_browsing()
            self._update_uifb()
        return self.get()

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
        return self.get()

    def add_atom(self, predicate):
        """
        Policy: Adds an assumption and basically resets the rest of the application (reground) -
        finally it returns the udpated Json structure.
        """
        predicate_symbol = parse_term(predicate)
        if predicate_symbol not in self._atoms:
            self._atoms.add(predicate_symbol)
            # Maybe best to do using the callback tuple?
            self._init_ctl()
            self._ground()
            self._end_browsing()
            self._update_uifb()
        return self.get()

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
        return self.get()

    def set_external(self, predicate, value):
        """
        Policy: Sets the value of an external.
        """
        symbol = parse_term(predicate)
        name = value
        self._end_browsing()

        if name == "release":
            self._ctl.release_external(parse_term(predicate))
            self._externals["released"].add(symbol)

            if symbol in self._externals["true"]:
                self._externals["true"].remove(symbol)

            if symbol in self._externals["false"]:
                self._externals["false"].remove(symbol)

        elif name == "true":
            self._ctl.assign_external(parse_term(predicate), True)
            self._externals["true"].add(symbol)

            if symbol in self._externals["false"]:
                self._externals["false"].remove(symbol)

        elif name == "false":
            self._ctl.assign_external(parse_term(predicate), False)
            self._externals["false"].add(symbol)

            if symbol in self._externals["true"]:
                self._externals["true"].remove(symbol)

        else:
            raise ValueError(
                f"Invalid external value {name}. Must be true, false or relase"
            )

        self._update_uifb()
        return self.get()

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
            self._handler = self._ctl.solve(
                assumptions=[(a, True) for a in self._assumptions], yield_=True
            )
            self._iterator = iter(self._handler)
        try:
            model = next(self._iterator)
            while optimizing and not model.optimality_proven:
                self._logger.info("Skipping non-optimal model")
                model = next(self._iterator)
            self._uifb.set_auto_conseq(model.symbols(shown=True, atoms=True))
            self._update_uifb_ui()
        except StopIteration:
            self._logger.info("No more solutions")
            self._end_browsing()
            self._update_uifb()
            self._uifb.add_message("Browsing Information", "No more solutions")

        return self.get()

    def select(self):
        """
        Policy: Select the current solution during browsing
        """
        self._end_browsing()
        last_model_symbols = self._uifb.get_auto_conseq()
        symbols_to_ignore = self._externals["true"]
        symbols_to_ignore.union(self._externals["false"])
        for s in last_model_symbols:  # pylint: disable=E1133
            if s not in symbols_to_ignore:
                self._add_assumption(s)
        self._update_uifb()
        return self.get()
