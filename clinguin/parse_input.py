import argparse
import importlib
import sys
import os
import inspect

from typing import Sequence, Any

class ArgumentParser():
    def __init__(self) -> None:
        pass

    def parse(self):

        parser = self._createParser()
        subparsers = parser.add_subparsers(help='sub-command help')

        parser_client = self._createClientSubparser(subparsers)
        parser_server = self._createServerSubparser(subparsers)
        parser_client_server = self._createClientServerSubparser(subparsers)

        args, unknown_args = parser.parse_known_args()

        return_dict = {}
        return_dict['method'] = args.method

        if args.method == 'server' or args.method == 'client-server':
            solver = self._importSolver(args.solver)    

            self._addSolverArgumentsToParser(solver, parser_server)
            self._addSolverArgumentsToParser(solver, parser_client_server)
            
            args, unknown_args = parser.parse_known_args()
            if len(unknown_args) != 0:
                print("[WARN (Pre-Logging-Phase)]: Could not parse arguments: " + str(unknown_args))
            return_dict = vars(args)
            return_dict['solver'] = solver
        
        return return_dict

    def _createParser(self):
        parser = argparse.ArgumentParser(description = 'Clinguin is a GUI language extension for a logic program that uses Clingo.')
        return parser

    def _createClientSubparser(self, subparsers):
        parser_client = subparsers.add_parser('client')
        parser_client.set_defaults(method='client')

        return parser_client
        
    def _createServerSubparser(self, subparsers):
        parser_server = subparsers.add_parser('server')
        parser_server.add_argument('--solver', type = str, nargs = 1, help = 'Optionally specify which solver(s) to use (seperate solvers by \',\'')
        parser_server.set_defaults(method='server')

        return parser_server

    def _createClientServerSubparser(self, subparsers):
        parser_server_client = subparsers.add_parser('client-server')
        parser_server_client.add_argument('--solver', type = str, nargs = 1, help = 'Optionally specify which solver(s) to use (seperate solvers by \',\'')
        parser_server_client.set_defaults(method='client-server')

        return parser_server_client

    def _addSolverArgumentsToParser(self, solvers, subparser):
        for solver in solvers:
            if hasattr(solver, '_registerOptions'):
                opt_function_signature = inspect.getargspec(solver._registerOptions)
                # [0] = args, [1] = varargs, [2] = keywords
                if len(opt_function_signature[0]) == 2 and\
                    opt_function_signature[1] == None and\
                        opt_function_signature[2] == None:
                    solver._registerOptions(subparser)


    def _importSolver(self, solver_paths : Sequence[str]) -> Sequence[any]:
        solvers = []
        default_solver_lib = 'clinguin.server.application.standard_solver'
        default_solver_class = 'ClingoBackend'

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

