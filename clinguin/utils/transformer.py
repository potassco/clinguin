"""
A clingo transformer that checks if files are using a given predicate signature
"""

import clingo.ast as _ast


class UsesSignatureTransformer(_ast.Transformer):
    """
    A transformer that checks if files are using a given predicate signature
    """

    def __init__(self, name: str, arity: int) -> None:
        self.name = name
        self.arity = arity
        self.contained = False

    def visit_Function(self, node: _ast.AST) -> _ast.AST:
        """
        Visits a function node and checks if it is the predicate signature we are looking for
        """
        if node.name == self.name and len(node.arguments) == self.arity:
            self.contained = True
        return node

    def parse_files(self, paths) -> str:
        """
        Parses the files and returns a string with the transformed program.
        """
        # pylint: disable=unnecessary-lambda
        _ast.parse_files([str(p) for p in paths], lambda stm: self(stm))
