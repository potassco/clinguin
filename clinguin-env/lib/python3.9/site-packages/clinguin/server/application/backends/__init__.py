"""
Module that contains the backends
"""

# pylint: disable=cyclic-import
from clinguin.server.application.backends.clingo_backend import ClingoBackend
from clinguin.server.application.backends.clingodl_backend import ClingoDLBackend
from clinguin.server.application.backends.clingraph_backend import ClingraphBackend
from clinguin.server.application.backends.explanation_backend import ExplanationBackend

__all__ = [
    ClingoBackend.__name__,
    ClingraphBackend.__name__,
    ExplanationBackend.__name__,
    ClingoBackend.__name__,
    ClingoDLBackend.__name__,
]
