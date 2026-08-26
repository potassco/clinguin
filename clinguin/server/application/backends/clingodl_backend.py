"""
Module that contains the ClingoDL Backend.
"""

import warnings

try:
    from clingodl import ClingoDLTheory

    _HAS_CLINGODL = True
except ImportError:
    _HAS_CLINGODL = False
    ClingoDLTheory = None
    warnings.warn(
        "clingodl is not installed. The ClingoDLBackend will not work until you "
        "install it (e.g. `pip install git+https://github.com/potassco/clingo-dl.git`).",
        ImportWarning,
    )

from clinguin.server.application.backends.theory_backend import TheoryBackend


class ClingoDLBackend(TheoryBackend):
    """
    Backend that allows programs using clingodl theory atoms as input.
    It also includes the assignment in the domain state.
    """

    theory_class = ClingoDLTheory

    def __init__(self, *args, **kwargs):
        if not _HAS_CLINGODL:
            raise ImportError(
                "clingodl is not installed. The ClingoDLBackend will not work until you "
                "install it (e.g. `pip install git+https://github.com/potassco/clingo-dl.git`)."
            )
        super().__init__(*args, **kwargs)
