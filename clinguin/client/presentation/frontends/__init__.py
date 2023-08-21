"""
module that contains all frontends
"""
from .tkinter_frontend.tkinter_frontend import TkinterFrontend
from .ipython_frontend.ipython_frontend import IPythonFrontend
from .angular_frontend.AngularFrontend import AngularFrontend

__all__ = [TkinterFrontend.__name__, IPythonFrontend.__name__, AngularFrontend.__name__ ]
