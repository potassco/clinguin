"""
Module that contains the ClingoBackend.
"""
import sys

from clingo import Control, parse_term
from clingo.script import enable_python
# Self defined
from clinguin.utils.errors import NoModelError
from clinguin.server import StandardJsonEncoder
from clinguin.server import ClinguinModel
from clinguin.server import ClinguinBackend
from clinguin.server.application.default_backends.standard_utils.brave_cautious_helper import *


enable_python()

class ClingoBackend(ClinguinBackend):
    """
    The ClingoBackend class is the backend that is selected by default. It provides basic functionality to argue bravely and cautiously. Further it provides several policies for assumptions, atoms and externals.
    """

    def __init__(self, args):
        super().__init__(args)

        self._source_files = args.source_files
        self._widget_files = args.widget_files
        
        # For browising
        self._handler=None
        self._iterator=None

        # To make static linters happy
        self._assumptions = None
        self._atoms = None
        self._ctl = None
        
        self._restart()
        
        # I think we should remove this and only have one ClinguinModel
        self._modelClass = ClinguinModel
        self._model=None

    @classmethod
    def register_options(cls, parser):
        parser.add_argument('--source-files', nargs='+', help='Files',metavar='')
        parser.add_argument('--widget-files', nargs='+', help='Files for the widget generation',metavar='')

    def _restart(self):
        self._end_browsing()
        self._assumptions = set()
        self._externals = {"true":set(),"false":set(),"released":set()}
        self._atoms = set()
        self._init_ctl()
        self._ground()

    def _init_ctl(self):
        self._ctl = Control(['0'])
        for f in self._source_files:
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

    def _update_model(self):
        try:
            self._model = ClinguinModel.from_widgets_file(
                self._ctl,
                self._widget_files, 
                self._assumptions)
        except NoModelError:
            self._model.add_message("Error","This operation can't be performed")

    def get(self):
        """
        Overwritten default method to get the gui as a Json structure.
        """
        if not self._model:
            self._update_model()

        json_structure =  StandardJsonEncoder.encode(self._model)

        return json_structure

    def clear_assumptions(self):
        """
        Policy: clear_assumptions removes all assumptions, then basically ''resets'' the backend (i.e. it regrounds, etc.) and finally updates the model and returns the updated gui as a Json structure.
        """
        self._end_browsing()
        self._assumptions = set()
        self._init_ctl()
        self._ground()

        self._update_model()
        return self.get()

    def add_assumption(self, predicate):
        """
        Policy: Adds an assumption and returns the udpated Json structure.
        """
        predicate_symbol = parse_term(predicate)
        if predicate_symbol not in self._assumptions:
            self._assumptions.add(predicate_symbol)
            self._end_browsing()
            self._update_model()
        return self.get()

    def remove_assumption(self, predicate):
        """
        Policy: Removes an assumption and returns the udpated Json structure.
        """
        # Iconf
        predicate_symbol = parse_term(predicate)
        if predicate_symbol in self._assumptions:
            self._assumptions.remove(predicate_symbol)
            self._end_browsing()
            self._update_model()
        return self.get()
   
    def remove_assumption_signature(self, predicate, arity):
        """
        Policy: removes predicates with the predicate name of predicate and the given arity
        """
        predicate_symbol = parse_term(predicate)
        to_remove = []
        for s in self._assumptions:
            if s.match(predicate_symbol.name, int(arity)):
                for i,a in enumerate(predicate_symbol.arguments):
                    if str(a)!='any' or s.arguments[i] != a:
                        break
                else:
                    continue
                
                to_remove.append(s)
        for s in to_remove:
            self._assumptions.remove(s)
        if len(to_remove)>0:
            self._end_browsing()
            self._update_model()
        return self.get()




    def clear_atoms(self):
        """
        Policy: clear_atoms removes all atoms, then basically ''resets'' the backend (i.e. it regrounds, etc.) and finally updates the model and returns the updated gui as a Json structure.
        """
        self._end_browsing()
        self._atoms = set()
        self._init_ctl()
        self._ground()

        self._update_model()
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
            self._update_model()
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
            self._update_model()
        return self.get()

    def set_external(self, predicate, value):
        """
        Policy: Sets the value of an external.
        """
        symbol = parse_term(predicate)
        name = value

        if name == "release":
            self._ctl.release_external(parse_term(predicate))
            self._externals["released"].add(symbol)

            if symbol in self._externals["true"]:
                self._externals["true"].remove(symbol)
    
            if symbol in self._externals["false"]:
                self._externals["false"].remove(symbol)

        elif name == "true":
            self._ctl.assign_external(parse_term(predicate),True)
            self._externals["true"].add(symbol)

            if symbol in self._externals["false"]:
                self._externals["false"].remove(symbol)

        elif name == "false":
            self._ctl.assign_external(parse_term(predicate),True)
            self._externals["false"].add(symbol)

            if symbol in self._externals["true"]:
                self._externals["true"].remove(symbol)

        else:
            raise ValueError(f"Invalid external value {name}. Must be true, false or relase")

        self._update_model()
        return self.get()

    def next_solution(self):
        if not self._iterator:
            self._ctl.configuration.solve.enum_mode = 'auto'
            self._handler = self._ctl.solve(
                assumptions=[(a,True) for a in self._assumptions],
                yield_=True)
            self._iterator = iter(self._handler)
        try:
            model = next(self._iterator)
            self._model = self._modelClass.from_clingo_model(model, self._widget_files)
        except StopIteration:
            self._logger.info("No more solutions")
            self._handler.cancel()
            self._update_model()
            self._model.add_message("Browsing Information","No more solutions")

        return self.get()
