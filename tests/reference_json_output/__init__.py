"""
This module contains the reference json output
"""

from .health import Health
from .basic_test_00 import BasicTest00
from .basic_test_01 import BasicTest01
from .basic_test_02 import BasicTest02
from .basic_test_03 import BasicTest03
from .basic_test_04 import BasicTest04
from .basic_test_05 import BasicTest05

__all__ = [Health.__name__, 
           BasicTest00.__name__, 
           BasicTest01.__name__, 
           BasicTest02.__name__, 
           BasicTest03.__name__, 
           BasicTest04.__name__,
           BasicTest05.__name__]

