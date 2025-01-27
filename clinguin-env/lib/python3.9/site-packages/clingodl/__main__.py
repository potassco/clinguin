#!/usr/bin/python
'''
This module provides an application class similar to clingo-dl plus a main
function to execute it.
'''

import sys
from typing import Callable, Sequence

from clingo import ast
from clingo.application import Application, ApplicationOptions, Flag, clingo_main
from clingo.control import Control
from clingo.script import enable_python
from clingo.solving import Model
from clingo.statistics import StatisticsMap
from clingo.symbol import Symbol, SymbolType

from . import ClingoDLTheory


class ClingoDLApp(Application):
    '''
    Application class similar to clingo-dl (excluding optimization).
    '''
    def __init__(self, name: str):
        self.__theory = ClingoDLTheory()
        self.program_name = name
        self.version = ".".join(str(x) for x in self.__theory.version())
        self._enable_python  = Flag()

    def register_options(self, options: ApplicationOptions):
        """
        Register clingo-dl related options.
        """
        options.add_flag("Basic Options", "enable-python", "Enable Python script tags", self._enable_python)
        self.__theory.register_options(options)

    def validate_options(self) -> bool:
        """
        Validate options.
        """
        self.__theory.validate_options()
        return True

    def print_model(self, model: Model, printer: Callable[[], None]):
        """
        Print assignment along with model.
        """
        # print model
        symbols = model.symbols(shown=True)
        sys.stdout.write(" ".join(str(symbol) for symbol in sorted(symbols) if not self.__hidden(symbol)))
        sys.stdout.write('\n')

        # print assignment
        sys.stdout.write('Assignment:\n')
        symbols = model.symbols(theory=True)
        assignment = []
        for symbol in sorted(symbols):
            if symbol.match("dl", 2):
                assignment.append("{}={}".format(*symbol.arguments))
        sys.stdout.write(" ".join(assignment))
        sys.stdout.write('\n')

        sys.stdout.flush()

    def main(self, control: Control, files: Sequence[str]):
        """
        Run clingo-dl application.
        """
        if self._enable_python:
            enable_python()

        self.__theory.register(control)

        with ast.ProgramBuilder(control) as bld:
            ast.parse_files(files, lambda stm: self.__theory.rewrite_ast(stm, bld.add))

        control.ground([("base", [])])
        self.__theory.prepare(control)

        control.solve(on_model=self.__on_model, on_statistics=self.__on_statistics)

    def __on_model(self, model: Model):
        """
        Pass model to theory.
        """
        self.__theory.on_model(model)

    def __on_statistics(self, step: StatisticsMap, accu: StatisticsMap):
        """
        Pass statistics to theory.
        """
        self.__theory.on_statistics(step, accu)

    def __hidden(self, symbol: Symbol):
        """
        Classify symbols starting with "__" as hidden.
        """
        return symbol.type == SymbolType.Function and symbol.name.startswith("__")


if __name__ == "__main__":
    sys.exit(int(clingo_main(ClingoDLApp("clingo-dl"), sys.argv[1:])))
