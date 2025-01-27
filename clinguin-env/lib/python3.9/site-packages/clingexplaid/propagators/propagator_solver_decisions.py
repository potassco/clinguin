"""
Propagator Module: Decision Order
"""

from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Sequence, Set, Tuple, Union

import clingo
from clingo import Propagator

INTERNAL_STRING = "INTERNAL"
POSITIVE_STRING = "[+]"
NEGATIVE_STRING = "[-]"


@dataclass
class Decision:
    """
    Dataclass representing a solver decision
    """

    positive: bool
    literal: int
    symbol: Optional[clingo.Symbol]

    def matches_any(self, signatures: Set[Tuple[str, int]], show_internal: bool = True) -> bool:
        """
        Checks if the decisions symbol matches any of the provided `signatures`. If  the decisions is an internal
        literal `show_internal` is returned.
        """
        if self.symbol is not None:
            for sig, arity in signatures:
                if self.symbol.match(sig, arity):
                    return True
        else:
            # show internal is show_internal is True
            return show_internal
        return False

    def __str__(self) -> str:
        symbol_string = str(self.symbol) if self.symbol is not None else INTERNAL_STRING
        sign_string = POSITIVE_STRING if self.positive else NEGATIVE_STRING
        return f"{sign_string} {symbol_string} [{self.literal}]"


class SolverDecisionPropagator(Propagator):
    """
    Propagator for showing the Solver Decisions of clingo
    """

    def __init__(
        self,
        signatures: Optional[Set[Tuple[str, int]]] = None,
        callback_propagate: Optional[Callable[[List[Union[Decision, List[Decision]]]], None]] = None,
        callback_undo: Optional[Callable[[], None]] = None,
    ):
        # pylint: disable=missing-function-docstring
        self.literal_symbol_lookup: Dict[int, clingo.Symbol] = {}
        self.signatures = signatures if signatures is not None else set()

        self.callback_propagate: Callable[[List[Union[Decision, List[Decision]]]], None] = (
            callback_propagate if callback_propagate is not None else lambda x: None
        )
        self.callback_undo: Callable[[], None] = callback_undo if callback_undo is not None else lambda: None

        self.last_decisions: List[Union[Decision, List[Decision]]] = []

    def init(self, init: clingo.PropagateInit) -> None:
        """
        Method to initialize the Decision Order Propagator. Here the literals are added to the Propagator's watch list.
        """
        for atom in init.symbolic_atoms:
            program_literal = atom.literal
            solver_literal = init.solver_literal(program_literal)
            self.literal_symbol_lookup[solver_literal] = atom.symbol

        for atom in init.symbolic_atoms:
            if len(self.signatures) > 0 and not any(atom.match(name=s, arity=a) for s, a in self.signatures):
                continue
            symbolic_atom = init.symbolic_atoms[atom.symbol]
            if symbolic_atom is None:
                continue  # nocoverage
            query_program_literal = symbolic_atom.literal
            query_solver_literal = init.solver_literal(query_program_literal)
            init.add_watch(query_solver_literal)
            init.add_watch(-query_solver_literal)

    def propagate(self, control: clingo.PropagateControl, changes: Sequence[int], use_diff: bool = True) -> None:
        """
        Propagate method the is called when one the registered literals is propagated by clasp. Here useful information
        about the decision progress is recorded to be visualized later.
        """
        # pylint: disable=unused-argument
        decisions, entailments = self.get_decisions(control.assignment)

        literal_sequence: List[Union[int, List[int]]] = []
        for d in decisions:
            literal_sequence.append(d)
            if d in entailments:
                literal_sequence.append(list(entailments[d]))

        decision_sequence = self.literal_to_decision_sequence(literal_sequence)

        if use_diff:
            decision_diff: List[Union[Decision, List[Decision]]] = []
            for i, decision in enumerate(decision_sequence):
                if i < len(self.last_decisions):
                    if self.last_decisions[i] != decision:
                        decision_diff.append(decision)
                else:
                    decision_diff.append(decision)
            self.last_decisions = decision_sequence
            self.callback_propagate(decision_diff)
        else:
            self.callback_propagate(decision_sequence)

    def undo(self, thread_id: int, assignment: clingo.Assignment, changes: Sequence[int]) -> None:
        """
        This function is called when one of the solvers decisions is undone.
        """
        # pylint: disable=unused-argument

        self.callback_undo()

    def literal_to_decision(self, literal: int) -> Decision:
        """
        Converts a literal integer to a `Decision` object.
        """
        is_positive = literal >= 0
        symbol = self.literal_symbol_lookup.get(abs(literal))
        return Decision(literal=abs(literal), positive=is_positive, symbol=symbol)

    def literal_to_decision_sequence(
        self, literal_sequence: List[Union[int, List[int]]]
    ) -> List[Union[Decision, List[Decision]]]:
        """
        Converts a literal sequence into a decision sequence. These sequences are made up of their respective types or
        lists of these types.
        """
        new_decision_sequence: List[Union[Decision, List[Decision]]] = []
        for element in literal_sequence:
            if isinstance(element, int):
                new_decision_sequence.append(self.literal_to_decision(element))
            elif isinstance(element, list):
                new_decision_sequence.append([self.literal_to_decision(literal) for literal in element])
        return new_decision_sequence

    @staticmethod
    def get_decisions(assignment: clingo.Assignment) -> Tuple[List[int], Dict[int, List[int]]]:
        """
        Helper function to extract a list of decisions and entailments from a clingo propagator assignment.
        """
        level = 0
        decisions = []
        entailments = {}
        try:
            while True:
                decision = assignment.decision(level)
                decisions.append(decision)

                trail = assignment.trail
                level_offset_start = trail.begin(level)
                level_offset_end = trail.end(level)
                level_offset_diff = level_offset_end - level_offset_start
                if level_offset_diff > 1:
                    entailments[decision] = trail[(level_offset_start + 1) : level_offset_end]
                level += 1
        except RuntimeError:
            return decisions, entailments
