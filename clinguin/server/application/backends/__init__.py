"""
Module that contains the default backends ClingoBackend, ClingraphBackend and TemporalBackend.
"""
from clinguin.server.application.backends.clingo_backend import ClingoBackend
from clinguin.server.application.backends.clingraph_backend import ClingraphBackend
from clinguin.server.application.backends.temporal_backend import TemporalBackend
from clinguin.server.application.backends.explanation_backend import ExplanationBackend
from clinguin.server.application.backends.clingraph_interactive_backend import ClingraphInteractiveBackend

__all__ = [ClingoBackend.__name__,
            ClingraphBackend.__name__,
            TemporalBackend.__name__,
            ExplanationBackend.__name__,
            ClingraphInteractiveBackend.__name__,
            ]

