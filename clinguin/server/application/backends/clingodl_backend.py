"""
Module that contains the ClingoDL Backend.
"""

from clingodl import ClingoDLTheory
from clinguin.server.application.backends.theory_backend import TheoryBackend


class ClingoDLBackend(TheoryBackend):
    """
    Backend that allows programs using clingodl theory atoms as input.
    It also includes the assignment in the domain state.
    """

    theory_class = ClingoDLTheory
