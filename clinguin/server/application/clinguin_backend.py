"""
Module which contains the ClinguinBackend.
"""
import logging

from clinguin.utils import CustomArgs

# Like an interface


class ClinguinBackend(CustomArgs):
    """
    Root class of all backends (here backend refers to the type like ClingoBackend, etc.). Just defines the logger, the standard arguments and get().
    """

    def __init__(self, args):
        self._logger = logging.getLogger(args.log_args['name'])
        self.args = args

    def get(self):
        pass
