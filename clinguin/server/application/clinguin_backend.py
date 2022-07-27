import logging

# Like an interface


class ClinguinBackend:

    def __init__(self, args):
        self._logger = logging.getLogger(args.log_args['name'])
        self.args = args

    @classmethod
    def registerOptions(cls, parser):
        pass

    def get(self):
        pass
