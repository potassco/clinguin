"""
Server module, contains core-program classes.
"""
from .presentation.endpoints import Endpoints
from .application.standard_json_encoder import StandardJsonEncoder
from .application.clinguin_backend import ClinguinBackend
from .data.uifb import UIFB

__all__ = [Endpoints.__name__, StandardJsonEncoder.__name__, ClinguinBackend.__name__, UIFB.__name__]


