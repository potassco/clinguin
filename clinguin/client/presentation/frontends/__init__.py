"""
module that contains all frontends
"""
from .tkinter_frontend.tkinter_frontend import TkinterFrontend
from .ipython_frontend.ipython_frontend import IPythonFrontend

__all__ = [TkinterFrontend.__name__, IPythonFrontend.__name__]
