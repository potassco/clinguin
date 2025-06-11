"""
Util functions for generating the domain state
"""

import functools
from functools import cached_property
from typing import List, Optional, Tuple, Union

import logging

from clingo import Control, parse_term, Symbol
from clingo.symbol import Function

from clinguin.utils.logging import domctl_log

log = logging.getLogger(__name__)


class DomainState:
    """
    A class to represent and construct the domain state while storing the cache.

    Attributes:
            _domain_state_constructors (list): A list to store the domain state constructors.
                The provided method needs to be annotated with ``@property`` or ``@cached_property``
            _backup_cache (dict): A dictionary to store the backup domain state cache.
    """

    def __init__(self, backend: "ClingoBackend"):  # type: ignore
        """
        Initializes the domain state constructors list and the backup cache dictionary.
        It also adds the default domain state constructors to the list.
        Is called only when the backend is first created.


        Arguments:
            method (str): Name of the property method

        Sets:


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
        self._backend = backend
        self._backup_cache = {}
        self._domain_state_constructors = [
            "_ds_context",
            "_ds_constants",
            "_ds_browsing",
            "_ds_cautious_optimal",
            "_ds_brave_optimal",
            "_ds_cautious",
            "_ds_brave",
            "_ds_model",  # Keep after brave and cautious
            "_ds_opt",
            "_ds_unsat",  # Keep after all solve calls
            "_ds_assume",
            "_ds_external",
            "_ds_atom",
        ]

    def clear_cache(self, methods: Optional[List[str]] = None):
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
                self._backup_cache[m] = self.__dict__[m]
                del self.__dict__[m]

    def _call_solver_with_cache(self, ds_id: str, ds_tag: str, models: int, opt_mode: str, enum_mode: str):
        """
        Generic function to call the using exiting cache on browsing.
        On UNSAT it returns the output saved in the cache

        Arguments:
            ds_id: Identifier used in the cache
        Returns:
            The program tagged
        """
        if self._backend._is_browsing:
            log.debug("Returning cache for %s", ds_id)
            return self._backup_cache[ds_id] if ds_id in self._backup_cache else ""
        log.debug(domctl_log(f'domctl.configuration.solve.models = {models}"'))
        log.debug(domctl_log(f'domctl.configuration.solve.opt_mode = {opt_mode}"'))
        log.debug(domctl_log(f'domctl.configuration.solve.enum_mode = {enum_mode}"'))
        self._backend._ctl.configuration.solve.models = models
        self._backend._ctl.configuration.solve.opt_mode = opt_mode
        self._backend._ctl.configuration.solve.enum_mode = enum_mode
        self._backend._prepare()
        log.debug(domctl_log(f"domctl.solve({[(str(a), b) for a, b in self._backend._assumption_list]}, yield_=True)"))
        symbols, ucore = self.solve(
            self._backend._ctl,
            self._backend._assumption_list,
            self._backend._on_model,
        )
        self._backend._unsat_core = ucore
        if symbols is None:
            log.warning("Got an UNSAT result with the given domain encoding.")
            return self._backup_cache[ds_id] if ds_id in self._backup_cache else ""
        return " ".join([str(s) + "." for s in list(self.tag(symbols, ds_tag))]) + "\n"

    @functools.lru_cache(maxsize=None)  # pylint: disable=[method-cache-max-size-none]
    def _ui_uses_predicate(self, name: str, arity: int):
        """
        Returns a truth value of weather the ui_files contain the given signature.

        Args:
            name (str): Predicate name
            arity (int): Predicate arity
        """
        return True
        # transformer = UsesSignatureTransformer(name, arity)
        # log.debug("Transformer parsing UI files to find %s/%s", name, arity)
        # transformer.parse_files(self._args.ui_files)
        # if not transformer.contained:
        #     log.debug("Predicate NOT contained. Domain constructor will be skipped")
        # return transformer.contained

    def get_domain_state(self):
        """
        Gets the domain state by calling all the domain constructor methods

        Some domain state constructors might skip the computation if the UI does not require them.
        """
        ds = ""
        for f in self._domain_state_constructors:
            ds += f"\n%%%%%%%% {f} %%%%%%%\n"
            ds += getattr(self, f)
        return ds

    def get_domain_state_dict(self):
        """
        Gets the domain state as a dictionary for the response of the server.

        Some domain state constructors might skip the computation if the UI does not require them.
        """
        ds = {}
        for f in self._domain_state_constructors:
            prg = getattr(self, f)
            ctl = Control(["0"])
            ctl.add("base", [], prg)
            ctl.ground([("base", [])])
            symbols = []
            with ctl.solve(yield_=True) as handle:
                for m in handle:
                    symbols = [str(a).replace('"', "'") for a in m.symbols(shown=True)]
            ds[f] = symbols
        return ds

    # -------- Domain state methods

    @property
    def _ds_context(self):
        """
        Adds context information from the client.

        Includes predicate  ``_clinguin_context/2`` indicating each key and value in the context.
        """
        prg = "#defined _clinguin_context/2. "
        for a in self._backend._context:
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
        It will use as optimality the mode set in the command line as `default-opt-mode` (`ignore` by default).

        It uses a cache that is erased after an operation makes changes in the control.
        """
        if self._backend._model is None:
            log.debug(domctl_log('domctl.configuration.solve.enum_mode = "auto"'))
            self._backend._ctl.configuration.solve.models = 1
            self._backend._ctl.configuration.solve.opt_mode = self._backend._args.default_opt_mode
            self._backend._ctl.configuration.solve.enum_mode = "auto"

            self._backend._prepare()
            log.debug(
                domctl_log(f"domctl.solve({[(str(a),b) for a,b in self._backend._assumption_list]}, yield_=True)")
            )

            symbols, ucore = self.solve(self._backend._ctl, self._backend._assumption_list, self._backend._on_model)
            self._backend._unsat_core = ucore
            if symbols is None:
                log.warning("Got an UNSAT result with the given domain encoding.")
                return (
                    self._backup_cache["_ds_model"] + "\n".join([str(a) + "." for a in self._backend._atoms])
                    if "_ds_model" in self._backup_cache
                    else ""
                )
            self._backend._model = symbols

        return " ".join([str(s) + "." for s in self._backend._model]) + "\n"

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

        return self._call_solver_with_cache("_ds_cautious", "_all", 0, "ignore", "cautious")

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

        return self._call_solver_with_cache("_ds_brave_optimal", "_any_opt", 0, "optN", "brave")

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

        return self._call_solver_with_cache("_ds_cautious_optimal", "_all_opt", 0, "optN", "cautious")

    @property
    def _ds_unsat(self):
        """
        Adds information about the statisfiablity of the domain control

        Includes predicate ``_clinguin_unsat/0`` if the domain control is unsat
        """
        prg = "#defined _clinguin_unsat/0. "
        if self._backend._unsat_core is not None:
            prg += "_clinguin_unsat."
        return prg + "\n"

    @property
    def _ds_browsing(self):
        """
        Adds information about the browsing state

        Includes predicate  ``_clinguin_browsing/0`` if the user is browsing solutions
        """
        prg = "#defined _clinguin_browsing/0. "
        if self._backend._is_browsing:
            prg += "_clinguin_browsing."
        return prg + "\n"

    @property
    def _ds_assume(self):
        """
        Adds information about the assumptions.

        Includes predicate  ``_clinguin_assume/2`` for every atom that was assumed,
        where the second argument is either true or false.
        """
        prg = "#defined _clinguin_assume/2. "
        for a, v in self._backend._assumption_list:
            v_str = "true" if v else "false"
            prg += f"_clinguin_assume({str(a)},{v_str}). "
        return prg + "\n"

    @property
    def _ds_atom(self):
        """
        Adds information about the added atoms.

        Includes predicate  ``_clinguin_atom/1`` for every atom that was added.
        """
        prg = "#defined _clinguin_atom/1. "
        for a in self._backend._atoms:
            prg += f"_clinguin_atom({str(a)}). "
        return prg + "\n"

    @property
    def _ds_external(self):
        """
        Adds information about the external atoms

        Includes predicate  ``_clinguin_external/2`` for every external atom that has been set.
        """
        prg = "#defined _clinguin_external/2. "
        for a in self._backend._externals["true"]:
            prg += f"_clinguin_external({str(a)},true). "
        for a in self._backend._externals["false"]:
            prg += f"_clinguin_external({str(a)},false). "
        for a in self._backend._externals["released"]:
            prg += f"_clinguin_external({str(a)},release). "
        return prg + "\n"

    @property
    def _ds_opt(self):
        """
        Adds program to pass with optimality information.

        Includes predicates:
         - ``_clinguin_cost/1``: With a single tuple indicating the cost of the current model
         - ``_clinguin_cost/2``: With the index and cost value, linearizing predicate ``_clinguin_cost/1``
         - ``_clinguin_optimal/0``: If the solution is optimal
         - ``_clinguin_optimizing/0``: If there is an optimization in the program
        """
        prg = "#defined _clinguin_cost/2. #defined _clinguin_cost/1. #defined _clinguin_optimal/1. "

        for i, c in enumerate(self._backend._cost):
            prg += f"_clinguin_cost({i},{c}). "
        if self._backend._optimal:
            prg += "_clinguin_optimal. "
        if self._backend._optimizing:
            prg += "_clinguin_optimizing. "

        prg += f"_clinguin_cost({tuple(self._backend._cost)}).\n"
        return prg

    @property
    def _ds_constants(self):
        """
        Adds constants  values.

        Includes predicate ``_clinguin_const/2`` for each constant provided
        in the command line and used in the domain files.
        """
        prg = "#defined _clinguin_const/2. "
        for k, v in self._backend._constants.items():
            prg += f"_clinguin_const({k},{v})."
        return prg + "\n"

    @staticmethod
    def tag(symbols: List[Symbol], tag_name: str):
        """
        Adds a predicate around all the symbols
        """
        if tag_name is None:
            return symbols
        tagged = []
        for s in symbols:
            tagged.append(Function(tag_name, [s]))
        return tagged

    @staticmethod
    def solve(ctl: Control, assumptions: List[Union[Tuple[Symbol, bool], int]], on_model=lambda m: None):
        """
        Adds information about the browsing to the domain state.

        Includes predicate  _clinguin_unsat/0
        """
        with ctl.solve(assumptions=assumptions, yield_=True) as result:
            model_symbols = None
            for m in result:
                on_model(m)
                model_symbols = m.symbols(shown=True, atoms=True, theory=True)
            if model_symbols is None:
                return None, result.core()
        return model_symbols, None
