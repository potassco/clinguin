"""
Module that contains the Clingcon Backend.
"""

import warnings

try:
    from clingcon import ClingconTheory

    _HAS_CLINGCON = True
except ImportError:
    _HAS_CLINGCON = False
    ClingconTheory = None
    warnings.warn(
        "clingcon is not installed. The ClingconBackend will not work until you "
        "install it (e.g. `pip install git+https://github.com/potassco/clingcon.git`).",
        ImportWarning,
    )

from clinguin.server.application.backends.theory_backend import TheoryBackend


class ClingconBackend(TheoryBackend):
    """
    Backend that allows programs using clingcon theory atoms as input.
    It also includes the assignment in the domain state.
    """

    theory_class = ClingconTheory

    def __init__(self, *args, **kwargs):
        if not _HAS_CLINGCON:
            raise ImportError(
                "clingodl is not installed. The ClingoDLBackend will not work until you "
                "install it (e.g. `pip install git+https://github.com/potassco/clingo-dl.git`)."
            )
        super().__init__(*args, **kwargs)
