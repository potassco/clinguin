"""
module that contains all frontends
"""
from .ipython_frontend.ipython_frontend import IPythonFrontend
from .tkinter_frontend.tkinter_frontend import TkinterFrontend

__all__ = [TkinterFrontend.__name__, IPythonFrontend.__name__]
