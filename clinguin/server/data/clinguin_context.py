"""
Clinguin Context passed to the clingo control object with helper python functions
"""

from clingo.symbol import String, SymbolType
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

    def __getattr__(self, name):
        # pylint: disable=import-outside-toplevel

        import __main__

        return getattr(__main__, name)
