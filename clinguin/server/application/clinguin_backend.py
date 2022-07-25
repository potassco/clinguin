import logging

# Like an interface
class ClinguinBackend:
    
    def __init__(self, parsed_config):
        self._logger = logging.getLogger(parsed_config['logger']['server']['name'])
        self._parsed_config = parsed_config

    @classmethod
    def _registerOptions(cls, parser):
        pass

    def _get(self):
        pass


