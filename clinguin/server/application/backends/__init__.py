"""
Module that contains the default backends ClingoMultishotBackend, ClingraphBackend and TemporalBackend.
"""

# pylint: disable=cyclic-import
from clinguin.server.application.backends.clingo_backend import ClingoBackend
from clinguin.server.application.backends.clingo_multishot_backend import (
    ClingoMultishotBackend,
)
from clinguin.server.application.backends.clingodl_backend import ClingoDLBackend
from clinguin.server.application.backends.clingraph_backend import ClingraphBackend
from clinguin.server.application.backends.explanation_backend import ExplanationBackend
from clinguin.server.application.backends.clingo_optimize_backend import (
    ClingoOptimizeBackend,
)

__all__ = [
    ClingoMultishotBackend.__name__,
    ClingraphBackend.__name__,
    ExplanationBackend.__name__,
    ClingoBackend.__name__,
    ClingoDLBackend.__name__,
    ClingoOptimizeBackend.__name__,
]
