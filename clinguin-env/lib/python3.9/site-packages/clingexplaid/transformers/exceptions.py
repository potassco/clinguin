"""
Exceptions for the Transformers Module
"""


class UntransformedException(Exception):
    """Exception raised if the get_assumptions method of an AssumptionTransformer is called before it is used to
    transform a program.
    """


class NotGroundedException(Exception):
    """Exception raised if the get_assumptions method of an AssumptionTransformer is called without the control object
    having been grounded beforehand.
    """
