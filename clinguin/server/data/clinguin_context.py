"""
Clinguin Context passed to the clingo control object with helper python functions
"""

from clingo.symbol import String, SymbolType


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
        return String("".join([str(x).strip('"') for x in args]))

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
        return String(s.string.format(*args_str))

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
