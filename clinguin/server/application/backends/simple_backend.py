"""
Module that contains the ClingoBackend.
"""
import sys

from clingo import Control, parse_term
from clingo.script import enable_python
# Self defined
from clinguin.utils.errors import NoModelError
from clinguin.server import StandardJsonEncoder
from clinguin.server import UIFB
from clinguin.server import ClinguinBackend
from clinguin.server.application.backends.standard_utils.brave_cautious_helper import *


enable_python()

class SimpleBackend(ClinguinBackend):
    """
    The ClingoBackend class is the backend that is selected by default. It provides basic functionality to argue bravely and cautiously. Further it provides several policies for assumptions, atoms and externals.
    """

    def __init__(self, args):
        super().__init__(args)

        self._domain_files = args.domain_files
        self._ui_files = args.ui_files

        # For browising
        self._handler=None
        self._iterator=None

        # To make static linters happy
        self._atoms = set()
        self._ctl = None

        self._end_browsing()
        self._atoms = set()
        self._constants = [f"-c {v}" for v in args.const] if args.const else []
        self._init_ctl()
        self._ground()

        include_unsat_msg = not args.ignore_unsat_msg
        self._uifb=UIFB(self._ui_files, self._constants, include_menu_bar=args.include_menu_bar, include_unsat_msg=include_unsat_msg)


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
        json_structure =  StandardJsonEncoder.encode(self._uifb)
        return json_structure

    @classmethod
    def register_options(cls, parser):
        parser.add_argument('--domain-files', nargs='+', help='Files',metavar='')
        parser.add_argument('--ui-files', nargs='+', help='Files for the element generation',metavar='')
        parser.add_argument('-c','--const',  nargs='+', help='Constant passed to clingo, <id>=<term> replaces term occurrences of <id> with <term>',metavar='')
        parser.add_argument('--include-menu-bar',
                    action='store_true',
                    help='Inlcude a menu bar with options: Next, Select and Clear')
        parser.add_argument('--ignore-unsat-msg',
                    action='store_true',
                    help='The automatic pop-up message in the UI when the domain files are UNSAT, will be ignored.')

    # ---------------------------------------------
    # Private methods
    # ---------------------------------------------

    def _init_ctl(self):
        self._ctl = Control(['0']+self._constants)
        for f in self._domain_files:
            try:
                self._ctl.load(str(f))
            except Exception as e:
                self._logger.critical(str(e))
                self._logger.critical("Failed to load modules (there is likely a syntax error in your logic program), now exiting - see previous stack trace for more information.")
                sys.exit()

        for atom in self._atoms:
            self._ctl.add("base",[],str(atom) + ".")


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
        state_prg = "#defined _clinguin_browsing/0. "
        if self._is_browsing:
            state_prg+="_clinguin_browsing."
        if self._uifb.is_unsat:
            state_prg+="_clinguin_unsat."
        return state_prg

    def _update_uifb_consequences(self):
        self._uifb.update_all_consequences(self._ctl, set())
        if self._uifb.is_unsat:
            self._logger.error("domain files are UNSAT. Setting _clinguin_unsat to true")

    def _update_uifb_ui(self):
        self._uifb.update_ui(self._backend_state_prg)

    def _update_uifb(self):
        self._update_uifb_consequences()
        self._update_uifb_ui()


    # ---------------------------------------------
    # Policies
    # ---------------------------------------------

    def clear_atoms(self):
        """
        Policy: clear_atoms removes all atoms, then basically ''resets'' the backend (i.e. it regrounds, etc.) and finally updates the model and returns the updated gui as a Json structure.
        """
        self._end_browsing()
        self._atoms = set()
        self._init_ctl()
        self._ground()

        self._update_uifb()
        return self.get()

    def add_atom(self, predicate):
        """
        Policy: Adds an assumption and basically resets the rest of the application (reground) - finally it returns the udpated Json structure.
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

    def remove_atom(self,predicate):
        """
        Policy: Removes an assumption and basically resets the rest of the application (reground) - finally it returns the udpated Json structure.
        """
        predicate_symbol = parse_term(predicate)
        if predicate_symbol in self._atoms:
            self._atoms.remove(predicate_symbol)
            self._init_ctl()
            self._ground()
            self._end_browsing()
            self._update_uifb()
        return self.get()

    def show_solution(self, opt_mode='ignore'):
        """
        Policy: Obtains the next solution
        Arguments:
            opt_mode: The clingo optimization mode, bu default is 'ignore', to browse only optimal models use 'optN'
        """
        self._init_ctl()
        self._ground()
        optimizing = opt_mode in ['optN','opt']
        self._ctl.configuration.solve.opt_mode = opt_mode
        self._ctl.configuration.solve.models = 0
        self._handler = self._ctl.solve(yield_=True)
        self._iterator = iter(self._handler)
        try:
            model = next(self._iterator)
            while optimizing and not model.optimality_proven:
                self._logger.info("Skipping non-optimal model")
                model = next(self._iterator)
            self._uifb.set_auto_conseq(model.symbols(shown=True,atoms=False))
            self._update_uifb_ui()
        except StopIteration:
            self._logger.info("No solutions")
            self._end_browsing()
            self._update_uifb()
            self._uifb.add_message("Browsing Information","No solutions")

        return self.get()
    

