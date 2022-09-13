"""
Module that contains the default backends ClingoBackend, ClingraphBackend and TemporalBackend.
"""
from clinguin.server.application.default_backends.clingo_backend import ClingoBackend
from clinguin.server.application.default_backends.clingraph_backend import ClingraphBackend
from clinguin.server.application.default_backends.temporal_backend import TemporalBackend
from clinguin.server.application.default_backends.explanation_backend import ExplanationBackend

__all__ = [ClingoBackend.__name__,
            ClingraphBackend.__name__,
            TemporalBackend.__name__,
            ExplanationBackend.__name__
            ]

