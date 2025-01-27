"""
Transformer Module: Split Rules into dedicated body and head parts
"""

import base64
from pathlib import Path
from typing import List, Union

import clingo
import clingo.ast as _ast


class RuleSplitter(_ast.Transformer):
    """
    A transformer that is used to split rules into two. This is done using an intermediate predicate called `_body`,
    which contains a base64 representation of the original rule and all body variable assignments for explanation
    purposes. This intermediate predicate replaces the head of the original rule and a new rule with the old head and
    the newly generated `_body` predicate as the body is also inserted. Use the `parse_string` method to apply this
    transformer.
    """

    def __init__(self) -> None:
        self.head_rules: List[clingo.ast.AST] = []

    def visit_Rule(self, node: clingo.ast.AST) -> clingo.ast.AST:  # pylint: disable=C0103
        """
        Replaces the head of every rule with the intermediate `_body` predicate and stores all new head rules using this
        intermediary predicate in `self.head_rules`
        """
        head = node.head
        body = node.body

        if body:
            # remove MUS literals from rule
            cleaned_body_literals = [x for x in node.body if x.atom.symbol.name not in ("__mus__",)]
            cleaned_body = "; ".join([str(l) for l in cleaned_body_literals])

            # get all variables used in body (to later reference in head)
            variables = set()
            for lit in cleaned_body_literals:
                arguments = lit.atom.symbol.arguments
                if arguments:
                    for arg in arguments:
                        variables.add(arg)

            # convert the cleaned body to a base64 string
            rule_body_string = cleaned_body
            rule_body_string_bytes = rule_body_string.encode("ascii")
            rule_body_base64_bytes = base64.b64encode(rule_body_string_bytes)
            rule_body_base64 = rule_body_base64_bytes.decode("ascii")

            # create a new '_body' head for the original rule
            new_head_arguments = [
                _ast.SymbolicTerm(node.location, clingo.parse_term(f'"{rule_body_base64}"')),
                _ast.Function(
                    location=node.location,
                    name="",
                    arguments=sorted(variables),
                    external=0,
                ),
            ]
            new_head = _ast.Function(
                location=node.location,
                name="_body",
                arguments=new_head_arguments,
                external=0,
            )
            node.head = new_head

            # create new second rule that links the head with the '_body' matching predicate
            new_head_rule = _ast.Rule(
                location=node.location,
                head=head,
                body=[new_head],
            )
            self.head_rules.append(new_head_rule)

            return node

        # default case
        return node

    def parse_string(self, string: str) -> str:
        """
        Function that applies the transformation to the `program_string` it's called with and returns the transformed
        program string.
        """
        self.head_rules = []
        out = []
        _ast.parse_string(string, lambda stm: out.append((str(self(stm)))))
        out += [str(r) for r in self.head_rules]

        return "\n".join(out)

    def parse_file(self, path: Union[str, Path], encoding: str = "utf-8") -> str:
        """
        Parses the file at path and returns a string with the transformed program.
        """
        with open(path, "r", encoding=encoding) as f:
            return self.parse_string(f.read())
