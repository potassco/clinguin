"""
Server module, contains core-program classes.
"""
from .application.clinguin_backend import ClinguinBackend
from .application.standard_json_encoder import StandardJsonEncoder
from .data.uifb import UIFB
from .presentation.endpoints import Endpoints

__all__ = [
    Endpoints.__name__,
    StandardJsonEncoder.__name__,
    ClinguinBackend.__name__,
    UIFB.__name__,
]
