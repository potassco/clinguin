"""
Transformer Module: Adding atoms to constraint heads to retrace the ones firing in the case of an unsatisfiable program.
"""

from pathlib import Path
from typing import Dict, Sequence, Union

import clingo
import clingo.ast as _ast


class ConstraintTransformer(_ast.Transformer):
    """
    A Transformer that takes all constraint rules and adds an atom to their head to avoid deriving false through them.
    """

    def __init__(self, constraint_head_symbol: str, include_id: bool = False):
        self._constraint_head_symbol = constraint_head_symbol
        self._include_id = include_id
        self._constraint_id = 1

        self.constraint_location_lookup: Dict[int, clingo.ast.Location] = {}

    def visit_Rule(self, node: clingo.ast.AST) -> clingo.ast.AST:  # pylint: disable=C0103
        """
        Adds a constraint_head_symbol atom to the head of every constraint.
        """
        if node.head.ast_type != _ast.ASTType.Literal:
            return node
        if node.head.atom.ast_type != _ast.ASTType.BooleanConstant:
            return node
        if node.head.atom.value != 0:
            return node

        arguments = []
        if self._include_id:
            arguments = [_ast.SymbolicTerm(node.location, clingo.parse_term(str(self._constraint_id)))]

        head_symbol = _ast.Function(
            location=node.location,
            name=self._constraint_head_symbol,
            arguments=arguments,
            external=0,
        )

        # add constraint location to lookup indexed by the constraint id
        self.constraint_location_lookup[self._constraint_id] = node.location

        # increase constraint id
        self._constraint_id += 1

        # insert id symbol into body of rule
        node.head = head_symbol
        return node.update(**self.visit_children(node))

    def parse_string(self, string: str) -> str:
        """
        Function that applies the transformation to the `program_string` it's called with and returns the transformed
        program string.
        """
        out = []
        _ast.parse_string(string, lambda stm: out.append((str(self(stm)))))

        return "\n".join(out)

    def parse_files(self, paths: Sequence[Union[str, Path]]) -> str:
        """
        Parses the files and returns a string with the transformed program.
        """
        out = []
        _ast.parse_files([str(p) for p in paths], lambda stm: out.append((str(self(stm)))))
        return "\n".join(out)
