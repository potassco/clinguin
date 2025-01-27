"""
Propagators for Explanation
"""

# pragma: no cover

from typing import List

from .propagator_solver_decisions import SolverDecisionPropagator

DecisionLevel = List[int]
DecisionLevelList = List[DecisionLevel]

__all__ = [
    "SolverDecisionPropagator",
]
