"""
This module provides different errors for clinguin.
"""

class NoModelError(Exception):
    """
    The NoModelError is raised, if the provided logic program is unsatisfiable.
    """
    def __init__(self, core=None) -> None:
        super().__init__()
        self.core = core
