"""
This module contains the reference json output
"""

from .basic_test_00 import BasicTest00
from .basic_test_01 import BasicTest01
from .basic_test_02 import BasicTest02
from .basic_test_03 import BasicTest03
from .basic_test_04 import BasicTest04
from .basic_test_05 import BasicTest05
from .basic_test_06 import BasicTest06
from .basic_test_07 import BasicTest07
from .basic_test_08 import BasicTest08
from .basic_test_09 import BasicTest09
from .basic_test_10 import BasicTest10
from .basic_test_11 import BasicTest11
from .basic_test_12 import BasicTest12
from .health import Health
from .sudoku import Sudoku

__all__ = [
    Health.__name__,
    BasicTest00.__name__,
    BasicTest01.__name__,
    BasicTest02.__name__,
    BasicTest03.__name__,
    BasicTest04.__name__,
    BasicTest05.__name__,
    BasicTest06.__name__,
    BasicTest07.__name__,
    BasicTest08.__name__,
    BasicTest09.__name__,
    BasicTest10.__name__,
    BasicTest11.__name__,
    BasicTest12.__name__,
    Sudoku.__name__,
]
