# pylint: disable=W0107
"""
The module contains the CustomArgs class.
"""


class CustomArgs:
    """
    The root class of all backend- (like ClingoBackend) and gui-classes (like TkinterFrontend).
    Needed for argparse (with the method register_options one can specify command line arguments,
    that are specific to a certain class).

    Method:
        register_options (parser: argparse-object)
    """

    @classmethod
    def register_options(cls, parser):
        """
        Method that needs to be implemented by all children.
        """
