import logging

# Like an interface
class ClinguinBackend:
    
    def __init__(self, args, log_dict):
        self._logger = logging.getLogger(log_dict['name'])
        self.args = args

    @classmethod
    def _registerOptions(cls, parser):
        pass

    def _get(self):
        pass


