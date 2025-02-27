"""
Util functions for generating the domain state
"""

from clingo.symbol import Function


def tag(symbols, tag_name):
    """
    Adds a predicate around all the symbols
    """
    if tag_name is None:
        return symbols
    tagged = []
    for s in symbols:
        tagged.append(Function(tag_name, [s]))
    return tagged


def solve(ctl, assumptions, on_model=lambda m: None):
    """
    Adds information about the browsing to the domain state.

    Includes predicate  _clinguin_unsat/0
    """
    with ctl.solve(assumptions=assumptions, yield_=True) as result:
        model_symbols = None
        for m in result:
            on_model(m)
            model_symbols = m.symbols(shown=True, atoms=True, theory=True)
        if model_symbols is None:
            return None, result.core()
    return model_symbols, None
