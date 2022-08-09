"""
Responsible for parsing the command line attributes
"""
import argparse
import importlib
import sys
import os
import inspect
import textwrap
import glob

from .server.application.clinguin_backend import ClinguinBackend
from .client.presentation.abstract_gui import AbstractGui
#from .client.presentation.tkinter.tkinter_gui import TkinterGui

class ArgumentParser():
    """
    ArgumentParser-Class, Responsible for parsing the command line attributes
    """
    
    default_solver_path = os.path.join('clinguin', 'server', 'application', 'default_solvers')
    default_client_path = os.path.join('clinguin', 'client', 'presentation', 'tkinter')

    default_solver = 'ClingoBackend'
    default_client = 'TkinterGui'

    def __init__(self) -> None:
        self.titles = {
            'client': self._client_title,
            'server': self._server_title,
            'client-server': self._client_server_title,
        }
        self.descriptions = {
            'client': 'Start a client process that will render a UI.',
            'server': 'Start server process making endpoints available for a client.',
            'client-server': 'Start client and a server processes.'}
        self.solver_name = None
        self.solver = None
        self._provide_help = False

    def parse(self):
        """
        After initialization of the ArgumentParser call this function to parse the arguments.
        """
        self._parseCustomClasses()

        if len(sys.argv) > 1:
            process = sys.argv[1]
        else:
            process = sys.argv[0]

        parser = argparse.ArgumentParser(description=self._clinguinDescription(
            process), add_help=True, formatter_class=argparse.RawTextHelpFormatter)
        subparsers = parser.add_subparsers(
            title="Process type",
            description='The type of process to start: a client (UI) a server (Backend) or both',
            dest='process')
        self._createClientSubparser(subparsers)
        self._createServerSubparser(subparsers)
        self._createClientServerSubparser(subparsers)
 
        args = parser.parse_args()

        self._addSelectedSolver(args)

        return args

    def _addSelectedSolver(self, args):
        args.solver = self.solver
        args.client = self.client

    @property
    def _clinguin_title(self):
        return '''
              ___| (_)_ __   __ _ _   _(_)_ __
             / __| | | '_ \\ / _` | | | | | '_ \\
            | (__| | | | | | (_| | |_| | | | | |
             \\___|_|_|_| |_|\\__, |\\__,_|_|_| |_|
                            |___/
            '''

    @property
    def _client_server_title(self):
        return '''
             _ | o  _  ._  _|_     _  _  ._     _  ._
            (_ | | (/_ | |  |_    _> (/_ |  \\/ (/_ |

            '''

    @property
    def _client_title(self):
        return '''
                       _ | o  _  ._  _|_
                      (_ | | (/_ | |  |_

            '''

    @property
    def _server_title(self):
        return '''
                       _  _  ._     _  ._
                      _> (/_ |  \\/ (/_ |

            '''

    def _clinguinDescription(self, process):
        description = 'Clinguin is a GUI language extension for a logic program that uses Clingo.'
        if process not in ['server', 'client', 'client-server']:
            ascci = f"{self._clinguin_title}{description}"
            return f"{inspect.cleandoc(ascci)}\n\n{description}"
        ascci = f"{self._clinguin_title}{self.titles[process]}"
        return f"{inspect.cleandoc(ascci)}\n\n{description}\n{self.descriptions[process]}"

    def _importClasses(self, path):
        sub_directories = ['']

        sys.path.append(path)

        """
        # Cant this be done like this instead? is simpler
        for name in glob.glob(path + '/*.py'):
            base = os.path.basename(name)
            file_name = os.path.splitext(base)[0]
            print(file_name)
            module = importlib.import_module(file_name)
        """

        self._recursiveImport(path, "", "")

    def _recursiveImport(self, full_path, rec_path, module):
        cur_path = os.path.join(full_path, rec_path)
 
        folder_paths = []
        file_paths = []

        for entity in os.scandir(os.path.join(full_path, rec_path)):
            if entity.is_dir():
                folder_paths.append(entity.path)
            elif entity.is_file():
                file_paths.append(entity.path)

        for file_path in file_paths:
            base = os.path.basename(file_path)
            file_name = os.path.splitext(base)[0]
            ending = os.path.splitext(base)[1]
            if ending == ".py":
                if module != "":
                    try:
                        importlib.import_module(module + "." + file_name)       
                    except:
                        print("Could not import module: " + module + "." + file_name)
                else: 
                    importlib.import_module(file_name)       

        for folder_path in folder_paths:
            base = os.path.basename(folder_path)
            new_module = module
            if new_module != "":
                new_module = new_module + "." + base
            else:
                new_module = base

            self._recursiveImport(full_path, os.path.join(rec_path, base), new_module)

    def _parseCustomClasses(self):
        custom_imports_parser = argparse.ArgumentParser(add_help=False)
        custom_imports_parser.add_argument('--custom-server-classes', type=str,
                                           help='Location of custom classes')
        self._addDefaultArgumentsToSolverParser(custom_imports_parser)
        
        custom_imports_parser.add_argument('--custom-client-classes', type=str,
                                           help='Location of custom classes')
        self._addDefaultArgumentsToClientParser(custom_imports_parser)

        args, unknown = custom_imports_parser.parse_known_args()
    
        self.client_name = args.client
        self.solver_name = args.solver
        if args.custom_server_classes:
            self._importClasses(args.custom_server_classes)
        else:
            self._importClasses(ArgumentParser.default_solver_path)

        if args.custom_client_classes:
            self._importClasses(args.custom_client_classes)
        else:
            self._importClasses(ArgumentParser.default_client_path)

        if '-h' in unknown or '--help' in unknown:
            self._provide_help = True

    def _createClientSubparser(self, subparsers):
        parser_client = subparsers.add_parser(
            'client',
            help=self.descriptions['client'],
            description=self._clinguinDescription('client'),
            add_help=True,
            formatter_class=argparse.RawTextHelpFormatter)

        self._addCustomClientsArguments(parser_client)

        self._addLogArguments(parser_client, abbrevation='C', logger_name = 'client')       

        self._addDefaultArgumentsToClientParser(parser_client)
        self.client = self._selectSubclassAndAddCustomArguments(parser_client, AbstractGui, self.client_name, ArgumentParser.default_client)

        return parser_client

    def _createServerSubparser(self, subparsers):
        parser_server = subparsers.add_parser(
            'server',
            help=self.descriptions['server'],
            description=self._clinguinDescription('server'),
            add_help=True,
            formatter_class=argparse.RawTextHelpFormatter)

        self._addCustomSolversArguments(parser_server)

        self._addLogArguments(parser_server, abbrevation='S', logger_name = 'server')       
        self._addDefaultArgumentsToSolverParser(parser_server)
        self.solver = self._selectSubclassAndAddCustomArguments(parser_server, ClinguinBackend, self.solver_name, ArgumentParser.default_solver)

        return parser_server

    def _createClientServerSubparser(self, subparsers):
        parser_server_client = subparsers.add_parser('client-server',
                                                     help=self.descriptions['client-server'],
                                                     description=self._clinguinDescription(
                                                         'client-server'),
                                                     add_help=True,
                                                     formatter_class=argparse.RawTextHelpFormatter)

        self._addCustomClientsArguments(parser_server_client)
        self._addCustomSolversArguments(parser_server_client)

        self._addLogArguments(parser_server_client, abbrevation='C', logger_name = 'client', display_name= 'client-')       
        self._addLogArguments(parser_server_client, abbrevation='S', logger_name = 'server', display_name ='server-')       

        self._addDefaultArgumentsToClientParser(parser_server_client)
        self.client = self._selectSubclassAndAddCustomArguments(parser_server_client, AbstractGui, self.client_name, ArgumentParser.default_client)

        self._addDefaultArgumentsToSolverParser(parser_server_client)
        self.solver = self._selectSubclassAndAddCustomArguments(parser_server_client, ClinguinBackend, self.solver_name, ArgumentParser.default_solver)

        return parser_server_client

    def _addDefaultArgumentsToSolverParser(self, parser):
        parser.add_argument('--solver', type=str,
                            help=textwrap.dedent('''\
                Optionally specify which solver to use using the class name.
                See available custom solvers bellow:
                '''),
                            metavar='')

    def _addDefaultArgumentsToClientParser(self, parser):
        parser.add_argument('--client', type=str,
                            help=textwrap.dedent('''\
                Optionally specify which client to use using the class name.
                See available custom clients bellow:
                '''),
                            metavar='')

    def _addLogArguments(self, parser, abbrevation='', logger_name = '', display_name=''):

        group = parser.add_argument_group(display_name + 'logger')
        group.add_argument('--' + display_name + 'log-disable-shell',
                                   action='store_true',
                                   help='Disable shell logging')
        group.add_argument('--' + display_name + 'log-disable-file',
                                   action='store_true',
                                   help='Disable file logging')
        group.add_argument('--' + display_name + 'logger-name',
                                   type=str,
                                   help='Set logger name',
                                   metavar='',
                                   default=logger_name)
        group.add_argument(
            '--' + display_name + 'log-level',
            type=str,
            help='Log level',
            metavar='',
            choices=[
                'DEBUG',
                'INFO',
                'ERROR',
                'WARNING'],
            default='DEBUG')
        group.add_argument(
            '--' + display_name + 'log-format-shell',
            type=str,
            help='Log format shell',
            metavar='',
            default='['+str(abbrevation)+'][%(levelname)s]<%(asctime)s>: %(message)s')
        group.add_argument(
            '--' + display_name + 'log-format-file',
            type=str,
            help='Log format file',
            metavar='',
            default='%(levelname)s<%(asctime)s>: %(message)s')

    def _addCustomSolversArguments(self, parser):
        parser.add_argument(
            '--custom-server-classes',
            type=str,
            help='Path to custom solver classes',
            metavar='')
 

    def _addCustomClientsArguments(self, parser):
       parser.add_argument(
            '--custom-client-classes',
            type=str,
            help='Path to custom client classes.',
            metavar='')


    def _selectSubclassAndAddCustomArguments(self, parser, parent, class_name, default_class):
        sub_classes = parent.__subclasses__()
        selected_class = None

        for sub_class in sub_classes:
            
            select_this_class_as_solver = (not class_name and sub_class.__name__ == default_class) or (sub_class.__name__ == class_name)
        
            if select_this_class_as_solver or self._provide_help == True:
                selected_class = sub_class
                group = parser.add_argument_group(sub_class.__name__)
                sub_class.registerOptions(group)

        return selected_class

