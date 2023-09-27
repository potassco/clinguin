"""
Module that contains the default backends ClingoMultishotBackend, ClingraphBackend and TemporalBackend.
"""
from clinguin.server.application.backends.clingo_backend import ClingoBackend
from clinguin.server.application.backends.clingo_multishot_backend import ClingoMultishotBackend
from clinguin.server.application.backends.clingraph_backend import ClingraphBackend
from clinguin.server.application.backends.explanation_backend import ExplanationBackend
from clinguin.server.application.backends.temporal_backend import TemporalBackend

__all__ = [
    ClingoMultishotBackend.__name__,
    ClingraphBackend.__name__,
    TemporalBackend.__name__,
    ExplanationBackend.__name__,
    ClingoBackend.__name__,
]
