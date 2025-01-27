"""
Transformer Module: Adding unique rule identifiers to the body of rules
"""

from pathlib import Path
from typing import Optional, Set, Tuple, Union

import clingo
import clingo.ast as _ast

from .constants import RULE_ID_SIGNATURE


class RuleIDTransformer(_ast.Transformer):
    """
    A Transformer that takes all the rules of a program and adds an atom with `self.rule_id_signature` in their bodys,
    to make the original rule the generated them identifiable even after grounding. Additionally, a choice rule
    containing all generated `self.rule_id_signature` atoms is added, which allows us to add assumptions that assume
    them. This is done in order to not modify the original program's reasoning by assuming all `self.rule_id_signature`
    atoms as True.
    """

    def __init__(self, rule_id_signature: str = RULE_ID_SIGNATURE):
        self.rule_id = 0
        self.rule_id_signature = rule_id_signature

    def visit_Rule(self, node: clingo.ast.AST) -> clingo.ast.AST:  # pylint: disable=C0103
        """
        Adds a rule_id_signature(id) atom to the body of every rule that is visited.
        """
        # add for each rule a theory atom (self.rule_id_signature) with the id as an argument
        symbol = _ast.Function(
            location=node.location,
            name=self.rule_id_signature,
            arguments=[_ast.SymbolicTerm(node.location, clingo.parse_term(str(self.rule_id)))],
            external=0,
        )

        # increase the rule_id by one after every transformed rule
        self.rule_id += 1

        # insert id symbol into body of rule
        node.body.insert(len(node.body), symbol)
        return node.update(**self.visit_children(node))

    def _get_number_of_rules(self) -> int:
        return self.rule_id - 1 if self.rule_id > 1 else self.rule_id

    def parse_string(self, string: str) -> str:
        """
        Function that applies the transformation to the `program_string` it's called with and returns the transformed
        program string.
        """
        self.rule_id = 1
        out = []
        _ast.parse_string(string, lambda stm: out.append((str(self(stm)))))
        out.append(
            f"{{_rule(1..{self._get_number_of_rules()})}}"
            f" % Choice rule to allow all _rule atoms to become assumptions"
        )

        return "\n".join(out)

    def parse_file(self, path: Union[str, Path], encoding: str = "utf-8") -> str:
        """
        Parses the file at path and returns a string with the transformed program.
        """
        with open(path, "r", encoding=encoding) as f:
            return self.parse_string(f.read())

    def get_assumptions(self, n_rules: Optional[int] = None) -> Set[Tuple[clingo.Symbol, bool]]:
        """
        Returns the rule_id_signature assumptions depending on the number of rules contained in the transformed
        program. Can only be called after parse_file has been executed before.
        """
        if n_rules is None:
            n_rules = self._get_number_of_rules()
        return {(clingo.parse_term(f"{self.rule_id_signature}({rule_id})"), True) for rule_id in range(1, n_rules + 1)}
