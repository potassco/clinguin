"""
module that contains all frontends
"""
from .angular_frontend.angular_frontend import AngularFrontend
from .ipython_frontend.ipython_frontend import IPythonFrontend
# from .tkinter_frontend.tkinter_frontend import TkinterFrontend

__all__ = [IPythonFrontend.__name__, AngularFrontend.__name__]  # TkinterFrontend.__name__
