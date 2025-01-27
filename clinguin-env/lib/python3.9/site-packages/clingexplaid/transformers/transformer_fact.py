"""
Transformer Module: Fact Remover
"""

from pathlib import Path
from typing import Optional, Sequence, Set, Tuple, Union

import clingo
from clingo import ast

from ..utils import match_ast_symbolic_atom_signature
from .constants import REMOVED_TOKEN


class FactTransformer(ast.Transformer):
    """
    Transformer that removes all facts from a program that match provided signatures
    """

    # pylint: disable=duplicate-code

    def __init__(self, signatures: Optional[Set[Tuple[str, int]]] = None):
        self.signatures = signatures if signatures is not None else set()

    def visit_Rule(self, node: clingo.ast.AST) -> clingo.ast.AST:  # pylint: disable=C0103
        """
        Removes all facts from a program that match the given signatures (if none are given all facts are removed).
        """
        if node.head.ast_type != ast.ASTType.Literal:
            return node
        if node.body:
            return node
        has_matching_signature = any(
            match_ast_symbolic_atom_signature(node.head.atom, (name, arity)) for (name, arity) in self.signatures
        )
        # if signatures are defined only transform facts that match them, else transform all facts
        if self.signatures and not has_matching_signature:
            return node

        return ast.Rule(
            location=node.location,
            head=ast.Function(location=node.location, name=REMOVED_TOKEN, arguments=[], external=0),
            body=[],
        )

    @staticmethod
    def post_transform(program_string: str) -> str:
        """
        Helper function that is called after the transformation process for cleanup purposes
        """
        # remove the transformed REMOVED_TOKENS from the resulting program string
        rules = program_string.split("\n")
        out = []
        for rule in rules:
            if not rule.startswith(REMOVED_TOKEN):
                out.append(rule)
        return "\n".join(out)

    def parse_string(self, string: str) -> str:
        """
        Function that applies the transformation to the `program_string` it's called with and returns the transformed
        program string.
        """
        out = []
        ast.parse_string(string, lambda stm: out.append(str(self(stm))))
        return self.post_transform("\n".join(out))

    def parse_files(self, paths: Sequence[Union[str, Path]]) -> str:
        """
        Parses the files and returns a string with the transformed program.
        """
        out = []
        ast.parse_files(
            [str(p) for p in paths],
            lambda stm: out.append(str(self(stm))),
        )
        return self.post_transform("\n".join(out))
