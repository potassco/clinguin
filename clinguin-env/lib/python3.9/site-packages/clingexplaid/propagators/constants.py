"""
Constant definitions for the propagators package
"""

from ..utils.logging import COLORS

UNKNOWN_SYMBOL_TOKEN = "INTERNAL"

INDENT_START = "├─"
INDENT_STEP = f"─{COLORS['GREY']}┼{COLORS['NORMAL']}──"
INDENT_END = f"─{COLORS['GREY']}┤{COLORS['NORMAL']}  "
