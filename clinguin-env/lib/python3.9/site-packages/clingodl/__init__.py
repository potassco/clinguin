'''
This module provides a clingo.Theory class for a DL theory.
'''

from clingo.theory import Theory
from ._clingodl import lib as _lib, ffi as _ffi

__all__ = ['ClingoDLTheory']


class ClingoDLTheory(Theory):
    '''
    The DL theory.
    '''
    def __init__(self):
        super().__init__("clingodl", _lib, _ffi)
