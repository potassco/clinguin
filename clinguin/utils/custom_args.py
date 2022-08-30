"""
The module contains the CustomArgs class.
"""

class CustomArgs:
    """
    The root class of all backend- (like ClingoBackend) and gui-classes (like TkinterGui). Needed for argparse (with the method registerOptions one can specify command line arguments, that are specific to a certain class).

    Method:
        registerOptions (parser: argparse-object)
    """

    @classmethod
    def registerOptions(cls, parser):
        pass




