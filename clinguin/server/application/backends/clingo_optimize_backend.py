"""
Module that contains the ClingoDL Backend.
"""

from clingo.script import enable_python
from functools import cached_property

from clinguin.server.application.backends.clingo_multishot_backend import (
    ClingoMultishotBackend,
)

from ....utils.logger import domctl_log
from clinguin.server.data.domain_state import solve, tag

enable_python()
# pylint: disable=attribute-defined-outside-init


class ClingoOptimizeBackend(ClingoMultishotBackend):
    """ """

    def __init__(self, args):
        super().__init__(args)

        # Model should be the last call so that the on_model takes the assignment of the model
        # and not of the cautious consequences
        self._domain_state_constructors.remove("_ds_model")
        self._add_domain_state_constructor("_ds_cautious_optimal")
        self._add_domain_state_constructor("_ds_brave_optimal")
        self._add_domain_state_constructor("_ds_model_optimal")

        self._add_domain_state_constructor("_ds_opt")

        self._cost = []  # Set in on_model
        self._optimal = False  # Set in on_model
        self._optimizing = False  # Set in on_model

    # ---------------------------------------------
    # Setups
    # ---------------------------------------------

    # ---------------------------------------------
    # Solving
    # ---------------------------------------------

    def _on_model(self, model):
        super()._on_model(model)
        self._optimizing = len(model.cost) > 0
        self._optimal = model.optimality_proven
        self._cost = model.cost

    # ---------------------------------------------
    # Domain state
    # ---------------------------------------------

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

    @cached_property
    def _ds_brave_optimal(self):
        """
        Computes brave consequences adds them as predicates ``_any/1``.

        It uses a cache that is erased after an operation makes changes in the control.
        """
        self._logger.debug("Getting Brave...")
        if self._is_browsing:
            return (
                self._backup_ds_cache["_ds_brave_optimal"]
                if "_ds_brave" in self._backup_ds_cache
                else ""
            )
        self._ctl.configuration.solve.models = 0
        self._ctl.configuration.solve.opt_mode = "optN"
        self._ctl.configuration.solve.enum_mode = "brave"
        self._logger.debug(domctl_log('domctl.configuration.solve.enum_mode = "brave"'))
        self._prepare()
        symbols, ucore = solve(
            self._ctl, [(a, True) for a in self._get_assumptions()], self._on_model
        )
        self._logger.debug(
            domctl_log(
                f"ctl.solve(assumptions={[(str(a), True) for a in self._get_assumptions()]}, yield_=True)"
            )
        )
        self._unsat_core = ucore
        if symbols is None:
            self._logger.warning("Got an UNSAT result with the given domain encoding.")
            return (
                self._backup_ds_cache["_ds_brave_optimal"]
                if "_ds_brave" in self._backup_ds_cache
                else ""
            )
        return " ".join([str(s) + "." for s in list(tag(symbols, "_any_opt"))]) + "\n"

    @cached_property
    def _ds_cautious_optimal(self):
        """
        Computes cautious consequences adds them as predicates ``_all/1``.

        It uses a cache that is erased after an operation makes changes in the control.
        """
        self._logger.debug("Getting Cautious...")
        if self._is_browsing:
            return (
                self._backup_ds_cache["_ds_cautious_optimal"]
                if "_ds_cautious" in self._backup_ds_cache
                else ""
            )
        self._ctl.configuration.solve.models = 0
        self._ctl.configuration.solve.opt_mode = "optN"
        self._ctl.configuration.solve.enum_mode = "cautious"
        self._logger.debug(
            domctl_log('domctl.configuration.solve.enum_mode = "cautious"')
        )
        self._prepare()
        symbols, ucore = solve(
            self._ctl, [(a, True) for a in self._get_assumptions()], self._on_model
        )
        self._logger.debug(
            domctl_log(
                f"ctl.solve(assumptions={[(str(a), True) for a in self._get_assumptions()]}, yield_=True)"
            )
        )
        self._unsat_core = ucore
        if symbols is None:
            self._logger.warning("Got an UNSAT result with the given domain encoding.")
            return (
                self._backup_ds_cache["_ds_cautious_optimal"]
                if "_ds_cautious" in self._backup_ds_cache
                else ""
            )

        return " ".join([str(s) + "." for s in list(tag(symbols, "_all_opt"))]) + "\n"

    @cached_property
    def _ds_model_optimal(self):
        """
        Computes a model if one has not been set yet.
        When the model is being iterated by the user, the current model is returned.
        It uses a cache that is erased after an operation makes changes in the control.
        """
        self._logger.debug("Getting Model...")
        if self._model is None:
            self._ctl.configuration.solve.models = 1
            self._ctl.configuration.solve.opt_mode = "optN"
            self._ctl.configuration.solve.enum_mode = "auto"
            self._logger.debug(
                domctl_log('domctlconfiguration.solve.enum_mode = "auto"')
            )

            self._prepare()
            symbols, ucore = solve(
                self._ctl, [(a, True) for a in self._get_assumptions()], self._on_model
            )
            self._logger.debug(
                domctl_log(
                    f"ctl.solve(assumptions={[(str(a), True) for a in self._get_assumptions()]}, yield_=True)"
                )
            )
            self._unsat_core = ucore
            if symbols is None:
                self._logger.warning(
                    "Got an UNSAT result with the given domain encoding."
                )
                return (
                    self._backup_ds_cache["_ds_model_optimal"]
                    + "\n".join([str(a) + "." for a in self._atoms])
                    if "_ds_model" in self._backup_ds_cache
                    else ""
                )
            self._model = symbols

        return " ".join([str(s) + "." for s in self._model]) + "\n"
