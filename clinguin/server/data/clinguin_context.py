"""
Clinguin Context passed to the clingo control object with helper python functions
"""

import hashlib
from clingo.symbol import String, SymbolType, Number
from clingo import parse_term


class ClinguinContext:
    """
    Makes available a set of python functions to be used in a UI encoding for handling strings.
    """

    def concat(self, *args):
        """
        Concatenates the given symbols as a string

        Example:
            .. code-block:: prolog

                attr(s_l(I), label, @concat("Semester ",I)):-semester(I).

            Label will be `Semester 1`
        Args:
            args: All symbols

        Returns:
            The string concatenating all symbols
        """
        new_atom = "".join([str(x).strip('"') for x in args])
        try:
            new_symbol = parse_term(new_atom)
        except Exception:
            new_symbol = String(new_atom)
        return new_symbol

    def format(self, s, *args):
        """
        Formats the string with the given arguments

        Example:
            .. code-block:: prolog

                attr(s_l(I), label, @format("Semester {}!",I)):-semester(I).

            Label will be `Semester 1!`

        Args:
            s (str): The string to format, for example "{0} and {1}"
            args: All symbols that can be accessed by the position starting in 0.
                If there is a single tuple as an argument, then its arguments are considered one by one.
        Returns:
            The string obtained by formatting the string with the given arguments
        """
        if (
            len(args) == 1
            and args[0].type == SymbolType.Function
            and args[0].name == ""
        ):
            args_str = [str(v).strip('"') for v in args[0].arguments]
        else:
            args_str = [str(v).strip('"') for v in args]
        new_atom = s.string.format(*args_str)
        try:
            new_symbol = parse_term(new_atom)
        except Exception:
            new_symbol = String(new_atom)
        return new_symbol

    def to_int(self, s):
        """
        Converts any symbol into an integer using a hash. It can be used to infer an order in the symbols
        for the `order` attribute in the UI.

        Example:
            .. code-block:: prolog

                attr(s_l(I), label, @to_int(person("Susana"))).

            Label will be `12`

        Args:
            s: The symbol to convert to an integer
        Returns:
            The integer value of the string
        """
        if s.type == SymbolType.Number:
            return s.number
        s = str(s)
        h = hashlib.sha256(s.encode()).hexdigest()
        return Number(int(h, 16) % 10**4)

    def replace(self, s, old, new):
        """
        Replaces all occurrences of the old string with the new string

        Example:
            .. code-block:: prolog

                attr(s_l(I), label, @replace("Semester 1", "1", "2")).

            Label will be `Semester 2`

        Args:
            s: The string to transform
            old: The string to replace
            new: The string to insert instead
        Returns:
            The string with the replaced values
        """
        val = str(s).strip('"')
        new_atom = val.replace(str(old).strip('"'), str(new).strip('"'))
        try:
            new_symbol = parse_term(new_atom)
        except Exception:
            new_symbol = String(new_atom)
        return new_symbol

    def stringify(self, s, capitalize=False):
        """
        Turns a value into a string without underscore and capitalized if requested

        Example:
            .. code-block:: prolog

                attr(s_l(I), label, @stringify(semester_1, true)). # Semester 1

            Label will be `Semester 1`

        Args:
            s: The value to transform
        Returns:
            The string without _
        """
        val = str(s).strip('"')
        val = val.replace("_", " ")
        if capitalize:
            val = val[0].upper() + val[1:]
        return String(val)

    def upper(self, s):
        """
        Turns a value into upper case

        Example:
            .. code-block:: prolog

                attr(s_l(I), label, @upper(semester_1)). # Semester 1

            Label will be `SEMESTER 1`

        Args:
            s: The value to transform
        Returns:
            The string without _
        """
        val = str(s).strip('"')
        return String(val.upper())

    def color(self, option, opacity=None):
        """
        Gets the html color code for the different options and the given opacity

        Args:
            option: primary, secondary, success, info, warning, danger, light
            opacity: Numeric value indicating the opacity of the color
        """
        option = str(option)
        opacity = str(opacity) if opacity is not None else None
        colors = {
            "primary": "#0052CC",
            "blue": "#0052CC",
            "secondary": "#6554C0",
            "purple": "#6554C0",
            "success": "#36B37E",
            "green": "#36B37E",
            "info": "#B3BAC5",
            "gray": "#B3BAC5",
            "warning": "#FFAB00",
            "yellow": "#FFAB00",
            "danger": "#FF5630",
            "red": "#FF5630",
            "light": "#F4F5F7",
        }
        if option not in colors:
            return String("#000000")

        hex_color = colors[option]

        if opacity is not None and opacity.isnumeric():
            o = int(opacity)
            if 0 <= o < 100:
                hex_color = f"{hex_color}{o:02d}"
        return String(hex_color)

    def __getattr__(self, name):
        # pylint: disable=import-outside-toplevel

        import __main__

        return getattr(__main__, name)
