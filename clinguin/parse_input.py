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
import traceback

from enum import Enum, auto

from .show_gui_syntax_enum import ShowGuiSyntaxEnum

from .server import ClinguinBackend
from .client import AbstractGui

class ArgumentParser():
    """
    ArgumentParser-Class, Responsible for parsing the command line attributes
    """

    default_backend_exec_string = "from .server.application.default_backends import *"    
    default_client_exec_string = "from .client.presentation.guis import *"

    default_backend = 'ClingoBackend'
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
        self.backend_name = None
        self.backend = None
        self._provide_help = False
        self._show_gui_syntax = ShowGuiSyntaxEnum.NONE

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

        self._addSelectedBackend(args)

        return args

    def _addSelectedBackend(self, args):
        args.backend = self.backend
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
        
        try:
            for entity in os.scandir(os.path.join(full_path, rec_path)):
                if entity.is_dir():
                    folder_paths.append(entity.path)
                elif entity.is_file():
                    file_paths.append(entity.path)
        except:
            print("<<<BEGIN-STACK-TRACE>>>")
            traceback.print_exc()
            print("<<<END-STACK-TRACE>>>")
            raise Exception("Could not find path for importing libraries: " + os.path.join(full_path, rec_path) + ". Therefore program is terminating now (full stacktrace is printed below).")
            

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
                        print("<<<BEGIN-STACK-TRACE>>>")
                        traceback.print_exc()
                        print("<<<END-STACK-TRACE>>>")
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

        self._addDefaultArgumentsToBackendParser(custom_imports_parser)
        self._addCustomBackendsArguments(custom_imports_parser)

        self._addDefaultArgumentsToClientParser(custom_imports_parser)
        self._addCustomClientsArguments(custom_imports_parser) 

        args, unknown = custom_imports_parser.parse_known_args()
    
        self.client_name = args.client
        self.backend_name = args.backend
        if args.custom_server_classes:
            self._importClasses(args.custom_server_classes)
        else:
            exec(ArgumentParser.default_backend_exec_string)

        if args.custom_client_classes:
            self._importClasses(args.custom_client_classes)
        else:
            exec(ArgumentParser.default_client_exec_string)

        if '-h' in unknown or '--help' in unknown or '--h' in unknown or '--he' in unknown or '--hel' in unknown:
            self._provide_help = True

        if args.gui_syntax and not args.gui_syntax_full:
            self._show_gui_syntax = ShowGuiSyntaxEnum.SHOW
        elif args.gui_syntax_full:
            self._show_gui_syntax = ShowGuiSyntaxEnum.FULL
        

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

        self._addCustomBackendsArguments(parser_server)

        self._addLogArguments(parser_server, abbrevation='S', logger_name = 'server')       
        self._addDefaultArgumentsToBackendParser(parser_server)
        self.backend = self._selectSubclassAndAddCustomArguments(parser_server, ClinguinBackend, self.backend_name, ArgumentParser.default_backend)

        return parser_server

    def _createClientServerSubparser(self, subparsers):
        parser_server_client = subparsers.add_parser('client-server',
                                                     help=self.descriptions['client-server'],
                                                     description=self._clinguinDescription(
                                                         'client-server'),
                                                     add_help=True,
                                                     formatter_class=argparse.RawTextHelpFormatter)

        self._addCustomClientsArguments(parser_server_client)
        self._addCustomBackendsArguments(parser_server_client)

        self._addLogArguments(parser_server_client, abbrevation='C', logger_name = 'client', display_name= 'client-')       
        self._addLogArguments(parser_server_client, abbrevation='S', logger_name = 'server', display_name ='server-')       

        self._addDefaultArgumentsToClientParser(parser_server_client)
        self.client = self._selectSubclassAndAddCustomArguments(parser_server_client, AbstractGui, self.client_name, ArgumentParser.default_client)

        self._addDefaultArgumentsToBackendParser(parser_server_client)
        self.backend = self._selectSubclassAndAddCustomArguments(parser_server_client, ClinguinBackend, self.backend_name, ArgumentParser.default_backend)

        return parser_server_client

    def _addDefaultArgumentsToBackendParser(self, parser):
        parser.add_argument('--backend', type=str,
                            help=textwrap.dedent('''\
                Optionally specify which backend to use using the class name.
                See available custom backends bellow:
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

    def _addCustomBackendsArguments(self, parser):
        parser.add_argument(
            '--custom-server-classes',
            type=str,
            help='Path to custom backend classes',
            metavar='')
 

    def _addCustomClientsArguments(self, parser):
        parser.add_argument(
            '--custom-client-classes',
            type=str,
            help='Path to custom client classes.',
            metavar='')
        parser.add_argument('--gui-syntax', 
                action='store_true',
                help='Show available commands for the GUI.')
        parser.add_argument('--gui-syntax-full', 
                action='store_true',
                help='Show available commands for the GUI and shows available value-types.')

    def _getSubClasses(self, cur_class):
        sub_classes = cur_class.__subclasses__()
        recursive = []
        for sub_class in sub_classes:
            recursive.extend(self._getSubClasses(sub_class))

        return sub_classes + recursive


    def _selectSubclassAndAddCustomArguments(self, parser, parent, class_name, default_class):
        sub_classes = self._getSubClasses(parent)
        
        selected_class = None

        for sub_class in sub_classes:
            full_class_name = sub_class.__name__
            
            select_this_class_as_backend = (not class_name and full_class_name == default_class) or (full_class_name == class_name)
        
            if select_this_class_as_backend or self._provide_help == True:
                if self._show_gui_syntax == ShowGuiSyntaxEnum.NONE:
                    group = parser.add_argument_group(full_class_name)
                    sub_class.registerOptions(group)
                elif hasattr(sub_class, 'availableSyntax'):
                    print(sub_class.availableSyntax(self._show_gui_syntax))
                    sys.exit()

                selected_class = sub_class

        return selected_class

