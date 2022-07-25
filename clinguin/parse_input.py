import argparse
import importlib
import sys
import os
import inspect
import textwrap
import inspect
from typing import Sequence, Any
from clinguin.server.application.clinguin_backend import ClinguinBackend
from clinguin.server.application.standard_solver import ClingoBackend
import glob

class ArgumentParser():
    
    def __init__(self) -> None:
        self.titles = {
            'client': self._client_title,
            'server': self._server_title,
            'client-server': self._client_server_title,
        }
        self.descriptions = {
            'client': 'Start a client process that will render a UI.',
            'server': 'Start server process making endpoints available for a client.',
            'client-server': 'Start client and a server processes.'
        }
        self.solver_name = None

    
    def parse(self):
        self._parseCustomClasses()
        
        return_dict = {}
        process = sys.argv[1]

        general_options_parser = self._createGeneralOptionsParser()
        parser = argparse.ArgumentParser(description = self.clinguin_description(process),
            add_help=True,
            formatter_class=argparse.RawTextHelpFormatter)
        subparsers = parser.add_subparsers(title="Process type",
            description='The type of process to start: a client (UI) a server (Backend) or both',
            dest='process')

        self._createClientSubparser(subparsers,general_options_parser)
        self._createServerSubparser(subparsers,general_options_parser)
        self._createClientServerSubparser(subparsers,general_options_parser)
        
        args = parser.parse_args()
        self._addSelectedSolver(args)

        return args

    def _addSelectedSolver(self,args):
        if 'solver' in args:
            args.solver=self.solver




    @property
    def _clinguin_title(self):
        return '''
              ___| (_)_ __   __ _ _   _(_)_ __  
             / __| | | '_ \ / _` | | | | | '_ \ 
            | (__| | | | | | (_| | |_| | | | | |
             \___|_|_|_| |_|\__, |\__,_|_|_| |_|
                            |___/  
            '''
    @property
    def _client_server_title(self):
        return '''
             _ |  _  o ._ _|_     _  _  ._    _  ._ 
            (_ | (/_ | | | |_    _> (/_ | \/ (/_ |   

            '''
    @property
    def _client_title(self):
        return '''
                       _ |  _  o ._ _|_
                      (_ | (/_ | | | |_

            '''
    @property    
    def _server_title(self):
        return '''
                       _  _  ._    _  ._ 
                      _> (/_ | \/ (/_ |   

            '''
    
    def clinguin_description(self, process):
        description = 'Clinguin is a GUI language extension for a logic program that uses Clingo.'
        if process not in ['server','client','client-server']:
            ascci = f"{self._clinguin_title}{description}"
            return f"{inspect.cleandoc(ascci)}\n\n{description}"
        ascci = f"{self._clinguin_title}{self.titles[process]}"
        return f"{inspect.cleandoc(ascci)}\n\n{description}\n{self.descriptions[process]}"


    def _importClasses(self, path):
        if path is None:
            return
        sys.path.append(path)
        for name in glob.glob(path + '/*.py'):
            base = os.path.basename(name)
            file_name = os.path.splitext(base)[0]
            module = importlib.import_module(file_name)

    
    def _parseCustomClasses(self):
        custom_imports_parser = argparse.ArgumentParser(add_help=False)
        custom_imports_parser.add_argument('--custom-classes', type = str,
            help = 'Location of custom classes')
        self._addDefaultArgumentsToSolverParser(custom_imports_parser)
        args, _ = custom_imports_parser.parse_known_args()
        self.solver_name = args.solver
        self._importClasses(args.custom_classes)    

    def _createGeneralOptionsParser(self):
        general_options_parser = argparse.ArgumentParser(add_help=True,
            formatter_class=argparse.RawTextHelpFormatter)
        general_options_parser.add_argument('--log-level', 
            type = str, 
            help = 'Log level',
            metavar='',
            choices=['DEBUG', 'INFO', 'ERROR', 'WARNING'],
            default='DEBUG')
        general_options_parser.add_argument('--log-format-shell', 
            type = str, 
            help = 'Log format shell',
            metavar='',
            default='[S][%(levelname)s]<%(asctime)s>: %(message)s')
        general_options_parser.add_argument('--log-format-file', 
            type = str, 
            help = 'Log format file',
            metavar='',
            default='%(levelname)s<%(asctime)s>: %(message)s')

        general_options_parser.add_argument('--custom-classes', type = str,
            help = 'Path to custom classes',metavar='')

        return general_options_parser


    def _createClientSubparser(self, subparsers,parent):
        parser_client = subparsers.add_parser('client', 
            help = self.descriptions['client'],
            description = self.clinguin_description('client'),
            add_help=False,
            parents=[parent],
            formatter_class=argparse.RawTextHelpFormatter)

        return parser_client
    
    def _createServerSubparser(self, subparsers,parent):
        parser_server = subparsers.add_parser('server', 
            help = self.descriptions['server'],
            description = self.clinguin_description('server'),
            add_help=False,
            parents=[parent],
            formatter_class=argparse.RawTextHelpFormatter)
        
        self._addDefaultArgumentsToSolverParser(parser_server)
        self._addCustomSolversArgumentsToParser(parser_server)


        return parser_server

    def _createClientServerSubparser(self, subparsers,parent):
        parser_server_client = subparsers.add_parser('client-server', 
            help = self.descriptions['client-server'],
            description = self.clinguin_description('client-server'),
            # help = "Starts a client and a server in different threads",
            add_help=False,
            parents=[parent],
            formatter_class=argparse.RawTextHelpFormatter)
        self._addDefaultArgumentsToSolverParser(parser_server_client)
        self._addCustomSolversArgumentsToParser(parser_server_client)

        return parser_server_client

    def _addDefaultArgumentsToSolverParser(self, parser):
        parser.add_argument('--solver', type = str, 
            help = textwrap.dedent('''\
                Optionally specify which solver to use using the class name.
                See available custom solvers bellow:
                '''),
            metavar='')

    def _addCustomSolversArgumentsToParser(self, parser):
        solvers = ClinguinBackend.__subclasses__()
        for solver in solvers:
            if not self.solver_name or solver.__name__ == self.solver_name:
                group = parser.add_argument_group(solver.__name__)
                solver._registerOptions(group)
            if solver.__name__ == self.solver_name:
                self.solver = solver

