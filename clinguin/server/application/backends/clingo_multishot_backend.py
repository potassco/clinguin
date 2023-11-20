# pylint: disable=R0801
"""
Module that contains the ClingoMultishotBackend.
"""

from clingo import parse_term
from clingo.script import enable_python

from clinguin.server.application.backends import ClingoBackend

enable_python()


class ClingoMultishotBackend(ClingoBackend):
    """
    Extends the basic clingo functionality for grounding and solving with the use of assumptions and externals.

    It is selected as the default Backend
    """

    # ---------------------------------------------
    # Required methods
    # ---------------------------------------------

    # ---------------------------------------------
    # Private methods
    # ---------------------------------------------

    def _init_setup(self):
        """
        Initializes the arguments when the server starts or after a restart.
        These arguments include, the handler and iterator for browsing answer sets,
        as well as the domain control, the atoms, assumptions and externals
        """
        super()._init_setup()
        # To make static linters happy
        self._assumptions = set()
        self._externals = {"true": set(), "false": set(), "released": set()}

    @property
    def _clinguin_state(self):
        """
        Creates the atoms that will be part of the clinguin state, which is passed to the UI computation.

        Includes predicates  _clinguin_browsing/0, _clinguin_context/2 and _clinguin_assume/1
        """
        prg = super()._clinguin_state
        state_prg = "#defined _clinguin_assume/1."
        for a in self._assumptions:
            state_prg += f"_clinguin_assume({str(a)})."
        return prg + state_prg

    @property
    def _output_prg(self):
        """
        Generates the output program used when downloading into a file.
        Includes all assumptions as facts.
        """
        prg = super()._output_prg
        for a in self._assumptions:
            prg = prg + f"{str(a)}.\n"
        return prg

    def _solve_set_handler(self):
        """
        Sets the solver handler by calling the solve method of clingo with the selected assumptions
        """
        # pylint: disable=attribute-defined-outside-init
        self._handler = self._ctl.solve(
            assumptions=[(a, True) for a in self._assumptions], yield_=True
        )

    def _add_assumption(self, predicate_symbol):
        """
        Adds an assumption to the set
        """
        self._assumptions.add(predicate_symbol)

    def _update_uifb_consequences(self):
        """
        Updates the brave and cautious consequences of the domain state, by calling clingo with the assumptions
        """
        self._uifb.update_all_consequences(self._ctl, self._assumptions, self._on_model)
        if self._uifb.is_unsat:
            self._logger.error(
                "domain files are UNSAT. Setting _clinguin_unsat to true"
            )

    # ---------------------------------------------
    # Policies
    # ---------------------------------------------

    def clear_assumptions(self):
        """
        Removes all assumptions.
        """
        self._end_browsing()
        # pylint: disable=attribute-defined-outside-init
        self._assumptions = set()

        self._update_uifb()

    def add_assumption(self, predicate):
        """
        Adds an assumption

        Arguments:

            predicate (str): The clingo symbol to be added
        """
        predicate_symbol = parse_term(predicate)
        if predicate_symbol not in self._assumptions:
            self._add_assumption(predicate_symbol)
            self._end_browsing()
            self._update_uifb()

    def remove_assumption(self, predicate):
        """
        Removes an assumption

        Arguments:

            predicate (str): The clingo symbol to be removed
        """
        predicate_symbol = parse_term(predicate)
        if predicate_symbol in self._assumptions:
            self._assumptions.remove(predicate_symbol)
            self._end_browsing()
            self._update_uifb()

    def remove_assumption_signature(self, predicate):
        """
        Removes predicates matching the predicate description.

        Arguments:

            predicate (str): The predicate description as a symbol,
                where the reserver word `any` is used to state that anything can
                take part of that position. For instance, `person(anna,any)`,
                will remove all assumptions of predicate person, where the first argument is anna.
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

    def set_external(self, predicate, value):
        """
        Sets the value of an external.

        Arguments:

            predicate (str): The clingo symbol to be set
            value (str): The value (release, true or false)
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

    def select(self):
        """
        Select the current solution during browsing.
        All atoms in the solution are added as assumptions in the backend.
        """
        self._end_browsing()
        last_model_symbols = self._uifb.get_auto_conseq()
        symbols_to_ignore = self._externals["true"]
        symbols_to_ignore.union(self._externals["false"])
        for s in last_model_symbols:  # pylint: disable=E1133
            if s not in symbols_to_ignore:
                self._add_assumption(s)
        self._update_uifb()
