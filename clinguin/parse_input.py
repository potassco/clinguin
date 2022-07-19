import argparse
import importlib
import sys
import os

from typing import Sequence, Any

class ArgumentParser():
    def __init__(self) -> None:
        pass

    def parse(self):

        args = self._parseArgs()

        source_files = self._checkSourceFilesExist(args.source_files)

        solvers = self._importSolver(args.solver)
        
        return (source_files, solvers)


    def _parseArgs(self) -> Any:
        parser = argparse.ArgumentParser(description = 'Clinguin is a GUI language extension for a logic program that uses Clingo.')

        parser.add_argument('--solver', type = str, nargs = '*', help = 'Optionally specify which solver(s) to use (seperate solvers by \',\'')
        parser.add_argument('source_files', nargs = '+', help = 'Specify at least one source file')

        args = parser.parse_args()
        
        return args


    def _checkSourceFilesExist(self, source_files : Sequence[str]) -> Sequence[str]:
        file_error = False
        for f in source_files:
            if os.path.exists(f) == False:
                file_error = True

        if file_error == True:
            print("File load error")
            sys.exit(1)

        return source_files


    def _importSolver(self, solver_paths : Sequence[str]) -> Sequence[any]:
        solvers = []
        default_solver_lib = 'clinguin.server.application.standard_solver'
        default_solver_class = 'StandardSolver'

        import_error = False
        if solver_paths == None or len(solver_paths) == 0:
            # Load default solver (default_solver)
            module = None
            (import_error, solvers) = self._loadSolver(default_solver_lib, default_solver_class, import_error, solvers)
        else:
            # Go through all provided solvers and load them
            for solver in solver_paths:
                module = None
                (library_path, class_name) = self._splitSolverString(solver)
                (import_error, solvers) = self._loadSolver(library_path, class_name, import_error, solvers)

        if import_error == True:
            print("Module import error")
            sys.exit(1)

        return solvers



    def _splitSolverString(self, solver) -> (str, str):

        split = solver.split('.')

        library_path = ''
        for i in range(0,len(split) - 1):
            if i == 0:
                library_path = split[i]
            else:
                library_path = library_path + '.' + split[i]

        className = split[len(split) - 1]

        return(library_path, className)

    def _loadSolver(self, library_path, class_name, import_error, solvers) -> (bool, Sequence[Any]):
        new_solvers = solvers.copy()
        print(library_path)
        module_spec = importlib.util.find_spec(library_path)
        if module_spec is not None:
            module = importlib.import_module(library_path)
            if hasattr(module, class_name):
                loaded_class = getattr(module, class_name)
                new_solvers.append(loaded_class)
                found = True
            else:
                import_error = True
        else:
            import_error = True

        return (import_error, new_solvers)

