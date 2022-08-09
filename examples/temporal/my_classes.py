from clinguin.server.application.clinguin_backend import ClinguinBackend

class TemporalBackend(ClinguinBackend):
    
    
    @classmethod
    def registerOptions(cls, parser):
        parser.add_argument('temporal_horizon', type=int)