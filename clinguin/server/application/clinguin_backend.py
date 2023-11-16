"""
Module which contains the ClinguinBackend.
"""
import logging

from clinguin.utils import CustomArgs

# Like an interface


class ClinguinBackend(CustomArgs):
    """
    Root class of all Backends. Sets up the logger, arguments and context.
    """

    def __init__(self, args):
        """
        Initializes the class by setting the logger arguments and context
        """
        self._logger = logging.getLogger(args.log_args["name"])
        self.args = args
        self.context = []

    def get(self, force_update=False):
        """
        Updates the UI and transforms the facts into a JSON.
        This method will be automatically called after executing all the operations.
        Thus, it needs to be implemented by all backends.
        """
        raise NotImplementedError("All backends must implement the method _get")

    def _set_context(self, context):
        """
        Sets the context

        Args:
            context: The context dictionary
        """
        self.context = context

    @classmethod
    def register_options(cls, parser):
        """
        Registers options in the command line for a given parser. It is automatically called on start for the provided backends.
        """
        pass