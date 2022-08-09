import logging

from clinguin.utils import CustomArgs

# Like an interface


class ClinguinBackend(CustomArgs):

    def __init__(self, args):
        self._logger = logging.getLogger(args.log_args['name'])
        self.args = args

    def get(self):
        pass
