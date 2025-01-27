"""
module that contains all frontends
"""

from .angular_frontend.angular_frontend import AngularFrontend

__all__ = [AngularFrontend.__name__]

try:
    from .tkinter_frontend.tkinter_frontend import TkinterFrontend

    __all__ += [TkinterFrontend.__name__]
except ImportError:
    # print("------> Tkinter needs has to be installed to use the TkinterFronted")
    pass
