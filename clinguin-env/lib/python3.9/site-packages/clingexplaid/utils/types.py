"""
Custom types for clingexplaid
"""

from typing import Iterable, Set, Tuple, Union

import clingo

SymbolSet = Set[clingo.Symbol]
Literal = Tuple[clingo.Symbol, bool]
LiteralSet = Set[Literal]
Assumption = Union[Literal, int]
AssumptionSet = Iterable[Assumption]
