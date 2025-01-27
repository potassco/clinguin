"""
This module contains the EnumType.
"""

from enum import Enum

from .type import Type


class EnumType(Type, Enum):
    """
    The EnumType shall not be directly used, only subtypes of the EnumType
    (like the ChildLayout) shall be used.
    """
