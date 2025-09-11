"""
Module that contains the Clingcon Backend.
"""

from clingcon import ClingconTheory
from clinguin.server.application.backends.theory_backend import TheoryBackend


class ClingconBackend(TheoryBackend):
    """
    Backend that allows programs using clingcon theory atoms as input.
    It also includes the assignment in the domain state.
    """

    theory_class = ClingconTheory
