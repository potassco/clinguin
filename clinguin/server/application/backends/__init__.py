"""
Module that contains the backends
"""

# pylint: disable=cyclic-import
from clinguin.server.application.backends.clingo_backend import ClingoBackend
from clinguin.server.application.backends.explanation_backend import ExplanationBackend
from clinguin.server.application.backends.clingraph_backend import ClingraphBackend

__all__ = [
    ClingoBackend.__name__,
    ClingraphBackend.__name__,
    ExplanationBackend.__name__,
    ClingoBackend.__name__,
]

try:
    from clinguin.server.application.backends.clingodl_backend import ClingoDLBackend

    __all__.append(ClingoDLBackend.__name__)
except ModuleNotFoundError:
    pass

try:
    from clinguin.server.application.backends.clingcon_backend import ClingconBackend

    __all__.append(ClingconBackend.__name__)
except ModuleNotFoundError:
    pass

try:
    from clinguin.server.application.backends.fclingo_backend import FclingoBackend

    __all__.append(FclingoBackend.__name__)
except ModuleNotFoundError:
    pass
