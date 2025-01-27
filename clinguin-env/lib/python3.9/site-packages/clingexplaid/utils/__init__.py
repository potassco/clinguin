"""
Utilities.
"""

import re
from typing import Dict, List, Set, Tuple

import clingo
from clingo.ast import ASTType


def match_ast_symbolic_atom_signature(ast_symbol: ASTType.SymbolicAtom, signature: Tuple[str, int]) -> bool:
    """
    Function to match the signature of an AST SymbolicAtom to a tuple containing a string and int value, representing a
    matching signature.
    """

    symbol = str(ast_symbol.symbol)
    name = symbol.split("(", maxsplit=1)[0]
    arity = len(ast_symbol.symbol.arguments)

    return all((signature[0] == name, signature[1] == arity))


def get_solver_literal_lookup(control: clingo.Control) -> Dict[int, clingo.Symbol]:
    """
    This function can be used to get a lookup dictionary to associate literal ids with their respective symbols for all
    symbolic atoms of the program
    """
    lookup = {}
    for atom in control.symbolic_atoms:
        lookup[atom.literal] = atom.symbol
    return lookup


__all__ = [
    match_ast_symbolic_atom_signature.__name__,
    get_solver_literal_lookup.__name__,
]


def get_signatures_from_model_string(model_string: str) -> Set[Tuple[str, int]]:
    """
    This function returns a dictionary of the signatures/arities of all atoms of a model string. Model strings are of
    the form: `"signature1(X1, ..., XN) ... signatureM(X1, ..., XK)"`
    """
    signatures = set()
    for atom_string in model_string.split():
        result = re.search(r"([^(]*)\(", atom_string)
        if result is None:
            signatures.add((atom_string, 0))
            continue
        signature = result.group(1)
        # calculate arity for the signature
        arity = 0
        level = 0
        for c in atom_string.removeprefix(signature):
            if c == "(":
                level += 1
            elif c == ")":
                level -= 1
            else:
                if level == 1 and c == ",":
                    arity += 1
        # if arity is not 0 increase by 1 for the last remaining parameter that is not followed by a comma
        # also increase arity by one for the case that there's only one parameter and no commas are contained just '('
        if arity > 0 or "(" in atom_string:
            arity += 1
        signatures.add((signature, arity))
    return signatures


def get_constants_from_arguments(argument_vector: List[str]) -> Dict[str, str]:
    """
    Function that is used to parse the command line argument vector to extract a dictionary of provided constants and
    their values. For example "-c test=42" would be converted to {"test": "42"}.
    """
    constants = {}
    next_constant = False
    for element in argument_vector:
        if next_constant:
            result = re.search(r"(.*)=(.*)", element)
            if result is None:
                continue
            constants[result.group(1)] = result.group(2)
            next_constant = False
        if element in ("-c", "--const"):
            next_constant = True

    return constants


def get_constant_string(name: str, value: str, prefix: str = "") -> str:
    """
    Create a constant string of the format "{prefix}{name}={value}".
    """
    constant_name_pattern = re.compile(r"^[a-zA-Z_].*")
    if not constant_name_pattern.match(name):
        raise ValueError("constant name does not abide to the naming standard")
    constr_string = f"{name}={value}"
    return prefix + constr_string
