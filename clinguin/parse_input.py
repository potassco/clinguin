"""
Responsible for parsing the command line attributes
"""
import argparse
import importlib
import sys
import os
import inspect
import textwrap
import traceback

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

        self.client_name = None
        self.client = None


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
        self._show_gui_syntax = ShowGuiSyntaxEnum.NONE

    def parse(self):
        """
        After initialization of the ArgumentParser call this function to parse the arguments.
        """
        self._parse_custom_classes()

        if len(sys.argv) > 1:
            process = sys.argv[1]
        else:
            process = sys.argv[0]

        parser = argparse.ArgumentParser(description=self._clinguin_description(
            process), add_help=True, formatter_class=argparse.RawTextHelpFormatter)
        subparsers = parser.add_subparsers(
            title="Process type",
            description='The type of process to start: a client (UI) a server (Backend) or both',
            dest='process')
        self._create_client_subparser(subparsers)
        self._create_server_subparser(subparsers)
        self._create_client_server_subparser(subparsers)
 
        args = parser.parse_args()

        self._add_selected_backend(args)

        return args

    def _add_selected_backend(self, args):
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

    def _clinguin_description(self, process):
        description = 'Clinguin is a GUI language extension for a logic program that uses Clingo.'
        if process not in ['server', 'client', 'client-server']:
            ascci = f"{self._clinguin_title}{description}"
            return f"{inspect.cleandoc(ascci)}\n\n{description}"
        else:
            ascci = f"{self._clinguin_title}{self.titles[process]}"
            return f"{inspect.cleandoc(ascci)}\n\n{description}\n{self.descriptions[process]}"

    def _import_classes(self, path):

        if os.path.isfile(path):
            sys.path.append(os.path.dirname(path))
            self._import_files_from_path_array([path])
        else: 
            sys.path.append(path)
            self._recursive_import(path, "", "")

    def _import_files_from_path_array(self,file_paths, module = ""):
        for file_path in file_paths:
            base = os.path.basename(file_path)
            file_name = os.path.splitext(base)[0]
            ending = os.path.splitext(base)[1]
            if ending == ".py":
                if module != "":
                    try:
                        importlib.import_module(module + "." + file_name)       
                    except Exception:
                        print("Could not import module: " + module + "." + file_name)
                        print("<<<BEGIN-STACK-TRACE>>>")
                        traceback.print_exc()
                        print("<<<END-STACK-TRACE>>>")
                else: 
                    importlib.import_module(file_name)       

    def _recursive_import(self, full_path, rec_path, module):
        folder_paths = []
        file_paths = []
        
        try:
            for entity in os.scandir(os.path.join(full_path, rec_path)):
                if entity.is_dir():
                    folder_paths.append(entity.path)
                elif entity.is_file():
                    file_paths.append(entity.path)
        except Exception:
            print("<<<BEGIN-STACK-TRACE>>>")
            traceback.print_exc()
            print("<<<END-STACK-TRACE>>>")
            raise Exception("Could not find path for importing libraries: " + os.path.join(full_path, rec_path) + ". Therefore program is terminating now (full stacktrace is printed below).")
            
        self._import_files_from_path_array(file_paths)

        for folder_path in folder_paths:
            base = os.path.basename(folder_path)
            new_module = module
            if new_module != "":
                new_module = new_module + "." + base
            else:
                new_module = base

            self._recursive_import(full_path, os.path.join(rec_path, base), new_module)

    def _parse_custom_classes(self):
        custom_imports_parser = argparse.ArgumentParser(add_help=False)
        self._add_default_arguments_to_backend_parser(custom_imports_parser)
        self._add_default_arguments_to_client_parser(custom_imports_parser)

        args, _ = custom_imports_parser.parse_known_args()
    
        self.client_name = args.client
        self.backend_name = args.backend
        if args.custom_classes:
            self._import_classes(args.custom_classes)

        exec(ArgumentParser.default_backend_exec_string)
        exec(ArgumentParser.default_client_exec_string)


        if args.gui_syntax and not args.gui_syntax_full:
            self._show_gui_syntax = ShowGuiSyntaxEnum.SHOW
        elif args.gui_syntax_full:
            self._show_gui_syntax = ShowGuiSyntaxEnum.FULL
        

    def _create_client_subparser(self, subparsers):
        parser_client = subparsers.add_parser(
            'client',
            help=self.descriptions['client'],
            description=self._clinguin_description('client'),
            add_help=True,
            formatter_class=argparse.RawTextHelpFormatter)

        self._add_log_arguments(parser_client, abbrevation='C', logger_name = 'clinguin_client')       

        self._add_default_arguments_to_client_parser(parser_client)
        self.client = self._select_subclass_and_add_custom_arguments(parser_client, AbstractGui, self.client_name, ArgumentParser.default_client)

        return parser_client

    def _create_server_subparser(self, subparsers):
        parser_server = subparsers.add_parser(
            'server',
            help=self.descriptions['server'],
            description=self._clinguin_description('server'),
            add_help=True,
            formatter_class=argparse.RawTextHelpFormatter)

        self._add_log_arguments(parser_server, abbrevation='S', logger_name = 'clinguin_server')       
        self._add_default_arguments_to_backend_parser(parser_server)
        self.backend = self._select_subclass_and_add_custom_arguments(parser_server, ClinguinBackend, self.backend_name, ArgumentParser.default_backend)

        return parser_server

    def _create_client_server_subparser(self, subparsers):
        parser_server_client = subparsers.add_parser('client-server',
                                                     help=self.descriptions['client-server'],
                                                     description=self._clinguin_description(
                                                         'client-server'),
                                                     add_help=True,
                                                     formatter_class=argparse.RawTextHelpFormatter)


        self._add_log_arguments(parser_server_client, abbrevation='C', logger_name = 'clinguin_client', display_name= 'client-')       
        self._add_log_arguments(parser_server_client, abbrevation='S', logger_name = 'clinguin_server', display_name ='server-')       

        self._add_default_arguments_to_client_parser(parser_server_client)
        self.client = self._select_subclass_and_add_custom_arguments(parser_server_client, AbstractGui, self.client_name, ArgumentParser.default_client)

        self._add_default_arguments_to_backend_parser(parser_server_client)
        self.backend = self._select_subclass_and_add_custom_arguments(parser_server_client, ClinguinBackend, self.backend_name, ArgumentParser.default_backend)

        return parser_server_client

    def _add_default_arguments_to_backend_parser(self, parser):
        sub_classes = self._get_sub_classes(ClinguinBackend)
        sub_class_as_options = "|".join([s.__name__ for s in sub_classes])
        sub_classes_str = "=>  Available options: {" + sub_class_as_options + "}"
        parser.add_argument('--backend', type=str,
                            help=textwrap.dedent(f'''\
                Optionally specify which backend to use using the class name.
                {sub_classes_str}
                '''),
                            metavar='')
        parser.add_argument(
            '--custom-classes',
            type=str,
            help='Path to custom classes.',
            metavar='')

    def _add_default_arguments_to_client_parser(self, parser):
        sub_classes = self._get_sub_classes(AbstractGui)
        sub_class_as_options = "|".join([s.__name__ for s in sub_classes])
        sub_classes_str = "=>  Available options: {" + sub_class_as_options + "}"
        parser.add_argument('--client', type=str,
                            help=textwrap.dedent(f'''\
                Optionally specify which client to use using the class name.
                {sub_classes_str}
                '''),
                            metavar='')
        parser.add_argument('--gui-syntax', 
                action='store_true',
                help='Show available commands for the GUI.')
        parser.add_argument('--gui-syntax-full', 
                action='store_true',
                help='Show available commands for the GUI and shows available value-types.')
        

    def _add_log_arguments(self, parser, abbrevation='', logger_name = '', display_name=''):

        group = parser.add_argument_group(display_name + 'logger')
        group.add_argument('--' + display_name + 'log-disable-shell',
                                   action='store_true',
                                   help='Disable shell logging')
        group.add_argument('--' + display_name + 'log-enable-file',
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
            default='INFO')
        group.add_argument(
            '--' + display_name + 'log-format-shell',
            type=str,
            help='Log format shell',
            metavar='',
            default='['+str(abbrevation)+'] %(levelname)s: %(message)s')
        group.add_argument(
            '--' + display_name + 'log-format-file',
            type=str,
            help='Log format file',
            metavar='',
            default='%(levelname)s: %(message)s')

  
    def _get_sub_classes(self, cur_class):
        sub_classes = cur_class.__subclasses__()
        recursive = []
        for sub_class in sub_classes:
            recursive.extend(self._get_sub_classes(sub_class))

        return sub_classes + recursive


    def _select_subclass_and_add_custom_arguments(self, parser, parent, class_name, default_class):
        sub_classes = self._get_sub_classes(parent)
        
        selected_class = None

        for sub_class in sub_classes:
            full_class_name = sub_class.__name__
            selected_by_default = not class_name and full_class_name == default_class
            selected =  full_class_name == class_name
            if selected_by_default or selected:
                group = parser.add_argument_group(full_class_name)
                sub_class.register_options(group)
        
                should_show_gui_syntax = self._show_gui_syntax == ShowGuiSyntaxEnum.SHOW or self._show_gui_syntax  == ShowGuiSyntaxEnum.FULL
                if should_show_gui_syntax and hasattr(sub_class, 'available_syntax'):
                    print(sub_class.available_syntax(self._show_gui_syntax))
                    sys.exit()

                selected_class = sub_class
        return selected_class

# W0703,R0201,W0707,W0122
