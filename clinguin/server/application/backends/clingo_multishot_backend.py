# pylint: disable=R0801
"""
Module that contains the ClingoMultishotBackend.
"""

from clingo import parse_term, Control
from clingo.script import enable_python

from clinguin.server.application.backends import ClingoBackend

enable_python()


class ClingoMultishotBackend(ClingoBackend):
    """
    Extends the basic clingo functionality for grounding and solving with the use of assumptions and externals.

    It is selected as the default Backend
    """

    def __init__(self, args):
        super().__init__(args)

        self._add_domain_state_constructor("_ds_assume")

    # ---------------------------------------------
    # Setups
    # ---------------------------------------------

    def _init_setup(self):
        """
        Initializes the arguments when the server starts or after a restart.
        These arguments include, the handler and iterator for browsing answer sets,
        as well as the domain control, the atoms, assumptions and externals
        """
        super()._init_setup()
        # To make static linters happy
        self._externals = {"true": set(), "false": set(), "released": set()}

    # ---------------------------------------------
    # Solving
    # ---------------------------------------------

    def _add_assumption(self, predicate_symbol):
        """
        Adds an assumption to the set
        """
        self._assumptions.add(predicate_symbol)

    # ---------------------------------------------
    # Domain state
    # ---------------------------------------------

    @property
    def _ds_assume(self):
        """
        Adds information about the assumptions

        Includes predicate  ``_clinguin_assume/1`` for every atom that was assumed.
        """
        prg = "#defined _clinguin_assume/1.\n"
        for a in self._get_assumptions():
            prg += f"_clinguin_assume({str(a)}).\n"
        return prg + "\n"

    ########################################################################################################

    # ---------------------------------------------
    # Public operations
    # ---------------------------------------------

    def clear_assumptions(self):
        """
        Removes all assumptions.
        """
        # pylint: disable=attribute-defined-outside-init
        self._outdate()
        self._assumptions = set()

    def add_assumption(self, atom):
        """
        Adds an atom `a` as an assumption.
        This assumption can be considered as an integrity constraint:
        `:- not a.` forcing the program to entail the given atom.

        Arguments:

            atom (str): The clingo symbol to be added as a true assumption
        """
        atom_symbol = parse_term(atom)
        if atom_symbol not in self._assumptions:
            self._add_assumption(atom_symbol)
            self._outdate()

    def remove_assumption(self, atom):
        """
        Removes an atom from the assumptions list.

        Arguments:

            atom (str): The clingo symbol to be removed
        """
        atom_symbol = parse_term(atom)
        if atom_symbol in self._assumptions:
            self._assumptions.remove(atom_symbol)
            self._outdate()

    def remove_assumption_signature(self, atom):
        """
        Removes from the list of assumptions those matching the given atom.
        Unlike function remove_assumption, this one allows for partial matches using the
        placeholder constant `any`

        Arguments:

            atom (str): The atom description as a symbol,
                where the reserver word `any` is used to state that anything can
                take part of that position. For instance, `person(anna,any)`,
                will remove all assumptions of atom person, where the first argument is anna.
        """
        atom_symbol = parse_term(atom)
        arity = len(atom_symbol.arguments)
        to_remove = []
        for s in self._assumptions:
            if s.match(atom_symbol.name, arity):
                for i, a in enumerate(atom_symbol.arguments):
                    if str(a) != "any" and s.arguments[i] != a:
                        break
                else:
                    to_remove.append(s)
                    continue
        for s in to_remove:
            self._assumptions.remove(s)
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

        if name == "release":
            self._ctl.release_external(parse_term(atom))
            self._externals["released"].add(symbol)

            if symbol in self._externals["true"]:
                self._externals["true"].remove(symbol)

            if symbol in self._externals["false"]:
                self._externals["false"].remove(symbol)

        elif name == "true":
            self._ctl.assign_external(parse_term(atom), True)
            self._externals["true"].add(symbol)

            if symbol in self._externals["false"]:
                self._externals["false"].remove(symbol)

        elif name == "false":
            self._ctl.assign_external(parse_term(atom), False)
            self._externals["false"].add(symbol)

            if symbol in self._externals["true"]:
                self._externals["true"].remove(symbol)

        else:
            raise ValueError(
                f"Invalid external value {name}. Must be true, false or relase"
            )

    def select(self, show_prg: str = ""):
        """
        Select the current solution during browsing.
        All atoms in the solution are added as assumptions in the backend.

        Arguments:

            show_program (str): An optional show program to filter atoms

        """
        if self._model is None:
            self._messages.append(
                ("No solution", "There is no solution to be selected", "danger")
            )
            self._logger.error(
                "No solution. No model has been computed that can be selected"
            )
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
                    raise Exception(
                        "Show program can't be parsed. Make sure it is a valid clingo program."
                    ) from exc
                prg = "\n".join([f"{str(s)}." for s in self._model])
                ctl.add("base", [], prg)
                ctl.ground([("base", [])])

                def add_shown(m):
                    for s in m.symbols(shown=True):
                        model.append(s)

                ctl.solve(on_model=add_shown)
            for s in model:  # pylint: disable=E1133
                if s not in symbols_to_ignore:
                    self._add_assumption(s)
        self._outdate()
