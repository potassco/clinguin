import logging

# Like an interface
class ClinguinBackend:
    
    def __init__(self, args):
        self._logger = logging.getLogger(args.log_args['name'])
        self.args = args

    @classmethod
    def _registerOptions(cls, parser):
        pass

    def _get(self):
        pass


