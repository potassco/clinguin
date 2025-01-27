"""
Responsible for parsing the command line attributes
"""

import argparse
import importlib
import inspect
import os
import sys
import textwrap
import traceback

from .client import AbstractFrontend
from .server.application.backends.clingo_backend import ClingoBackend
from .show_frontend_syntax_enum import ShowFrontendSyntaxEnum

if sys.version_info[1] < 8:
    import importlib_metadata as metadata  # nocoverage
else:
    from importlib import metadata  # nocoverage

VERSION = metadata.version("clinguin")


class ArgumentParser:
    """
    ArgumentParser-Class, Responsible for parsing the command line attributes
    """

    default_backend_exec_string = "from .server.application.backends import *"
    default_frontend_exec_string = "from .client.presentation.frontends import *"

    default_backend = "ClingoBackend"
    default_frontend = "AngularFrontend"

    def __init__(self) -> None:
        self.frontend_name = None
        self.frontend = None

        self.titles = {
            "client": self._client_title,
            "server": self._server_title,
            "client-server": self._client_server_title,
        }
        self.descriptions = {
            "client": "Start a client process that will render a UI.",
            "server": "Start server process making endpoints available for a client.",
            "client-server": "Start client and a server processes.",
        }
        self.backend_name = None
        self.backend = None
        self._show_frontend_syntax = ShowFrontendSyntaxEnum.NONE

    def parse(self, process, string_args):
        """
        After initialization of the ArgumentParser call this function to parse the arguments.
        """
        self._parse_custom_classes(string_args)

        parser = argparse.ArgumentParser(
            description=self._clinguin_description(process),
            add_help=True,
            formatter_class=argparse.RawTextHelpFormatter,
        )
        parser.add_argument(
            "--version", "-v", action="version", version=f"%(prog)s {VERSION}"
        )
        subparsers = parser.add_subparsers(
            title="Process type",
            description="The type of process to start: a client (UI) a server (Backend) or both",
            dest="process",
        )
        self._create_client_subparser(subparsers)
        self._create_server_subparser(subparsers)
        self._create_client_server_subparser(subparsers)

        args = parser.parse_args(string_args)

        self._add_selected_backend(args)

        return args

    def _add_selected_backend(self, args):
        args.backend = self.backend
        args.frontend = self.frontend

    @property
    def _clinguin_title(self):
        return """
              ___| (_)_ __   __ _ _   _(_)_ __
             / __| | | '_ \\ / _` | | | | | '_ \\
            | (__| | | | | | (_| | |_| | | | | |
             \\___|_|_|_| |_|\\__, |\\__,_|_|_| |_|
                            |___/
            """

    @property
    def _client_server_title(self):
        return """
             _ | o  _  ._  _|_     _  _  ._     _  ._
            (_ | | (/_ | |  |_    _> (/_ |  \\/ (/_ |

            """

    @property
    def _client_title(self):
        return """
                       _ | o  _  ._  _|_
                      (_ | | (/_ | |  |_

            """

    @property
    def _server_title(self):
        return """
                       _  _  ._     _  ._
                      _> (/_ |  \\/ (/_ |

            """

    def _clinguin_description(self, process):
        description = (
            "Clinguin is a GUI language extension for a logic program that uses Clingo."
        )
        if process not in ["server", "client", "client-server"]:
            ascci = f"{self._clinguin_title}{description}"
            return_value = f"{inspect.cleandoc(ascci)}\n\n{description}"
        else:
            ascci = f"{self._clinguin_title}{self.titles[process]}"
            return_value = f"{inspect.cleandoc(ascci)}\n\n{description}\n{self.descriptions[process]}"

        return return_value

    def _import_classes(self, path):
        if os.path.isfile(path):
            sys.path.append(os.path.dirname(path))
            self._import_files_from_path_array([path])
        else:
            sys.path.append(path)
            self._recursive_import(path, "", "")

    def _import_files_from_path_array(self, file_paths, module=""):
        for file_path in file_paths:
            base = os.path.basename(file_path)
            file_name = os.path.splitext(base)[0]
            ending = os.path.splitext(base)[1]
            if ending == ".py":
                if module != "":
                    try:
                        importlib.import_module(module + "." + file_name)
                    except Exception as ex:
                        raise Exception(
                            "Could not import module: " + module + "." + file_name
                        ) from ex
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
        except Exception as ex:
            print("<<<BEGIN-STACK-TRACE>>>")
            traceback.print_exc()
            print("<<<END-STACK-TRACE>>>")
            raise Exception(
                "Could not find path for importing libraries: "
                + os.path.join(full_path, rec_path)
                + ". Therefore program is terminating now (full stacktrace is printed below)."
            ) from ex

        self._import_files_from_path_array(file_paths)

        for folder_path in folder_paths:
            base = os.path.basename(folder_path)
            new_module = module
            if new_module != "":
                new_module = new_module + "." + base
            else:
                new_module = base

            self._recursive_import(full_path, os.path.join(rec_path, base), new_module)

    def _parse_custom_classes(self, str_args):
        custom_imports_parser = argparse.ArgumentParser(add_help=False)
        self._add_default_arguments_to_backend_parser(custom_imports_parser)
        self._add_default_arguments_to_client_parser(custom_imports_parser)

        args, _ = custom_imports_parser.parse_known_args(str_args)

        self.frontend_name = args.frontend
        self.backend_name = args.backend
        if args.custom_classes:
            self._import_classes(args.custom_classes)

        exec(ArgumentParser.default_backend_exec_string)
        exec(ArgumentParser.default_frontend_exec_string)

        if args.frontend_syntax and not args.frontend_syntax_full:
            self._show_frontend_syntax = ShowFrontendSyntaxEnum.SHOW
        elif args.frontend_syntax_full:
            self._show_frontend_syntax = ShowFrontendSyntaxEnum.FULL

    def _create_client_subparser(self, subparsers):
        parser_client = subparsers.add_parser(
            "client",
            help=self.descriptions["client"],
            description=self._clinguin_description("client"),
            add_help=True,
            formatter_class=argparse.RawTextHelpFormatter,
        )

        self._add_log_arguments(
            parser_client, abbrevation="C", logger_name="clinguin_client"
        )

        parser_client.add_argument(
            "--server-port",
            type=int,
            default=8000,
            help="Define the Port of the server, default value is 8000.",
        )

        parser_client.add_argument(
            "--server-url",
            type=str,
            default="http://localhost",
            help="Define the URL of the server, default value is 'http://localhost'.",
        )

        self._add_default_arguments_to_client_parser(parser_client)
        self.frontend = self._select_subclass_and_add_custom_arguments(
            parser_client,
            AbstractFrontend,
            self.frontend_name,
            ArgumentParser.default_frontend,
        )

        return parser_client

    def _create_server_subparser(self, subparsers):
        parser_server = subparsers.add_parser(
            "server",
            help=self.descriptions["server"],
            description=self._clinguin_description("server"),
            add_help=True,
            formatter_class=argparse.RawTextHelpFormatter,
        )

        self._add_log_arguments(
            parser_server, abbrevation="S", logger_name="clinguin_server"
        )
        self._add_default_arguments_to_backend_parser(parser_server)
        self.backend = self._select_subclass_and_add_custom_arguments(
            parser_server,
            ClingoBackend,
            self.backend_name,
            ArgumentParser.default_backend,
        )

        return parser_server

    def _create_client_server_subparser(self, subparsers):
        parser_server_client = subparsers.add_parser(
            "client-server",
            help=self.descriptions["client-server"],
            description=self._clinguin_description("client-server"),
            add_help=True,
            formatter_class=argparse.RawTextHelpFormatter,
        )

        self._add_log_arguments(
            parser_server_client,
            abbrevation="C",
            logger_name="clinguin_client",
            display_name="client-",
        )
        self._add_log_arguments(
            parser_server_client,
            abbrevation="S",
            logger_name="clinguin_server",
            display_name="server-",
        )

        self._add_default_arguments_to_client_parser(parser_server_client)
        self.frontend = self._select_subclass_and_add_custom_arguments(
            parser_server_client,
            AbstractFrontend,
            self.frontend_name,
            ArgumentParser.default_frontend,
        )

        self._add_default_arguments_to_backend_parser(parser_server_client)
        self.backend = self._select_subclass_and_add_custom_arguments(
            parser_server_client,
            ClingoBackend,
            self.backend_name,
            ArgumentParser.default_backend,
        )

        return parser_server_client

    def _add_default_arguments_to_backend_parser(self, parser):
        sub_classes = [ClingoBackend] + self._get_sub_classes(ClingoBackend)
        sub_class_as_options = "|".join([s.__name__ for s in sub_classes])
        sub_classes_str = "=>  Available options: {" + sub_class_as_options + "}"
        parser.add_argument(
            "--backend",
            type=str,
            help=textwrap.dedent(
                f"""\
                Optionally specify which backend to use using the class name.
                {sub_classes_str}
                """
            ),
            metavar="",
        )
        parser.add_argument(
            "--custom-classes", type=str, help="Path to custom classes.", metavar=""
        )
        parser.add_argument(
            "--server-port",
            type=int,
            default=8000,
            help="Define the server side port, default value is 8000.",
        )

    def _add_default_arguments_to_client_parser(self, parser):
        sub_classes = self._get_sub_classes(AbstractFrontend)
        sub_class_as_options = "|".join([s.__name__ for s in sub_classes])
        sub_classes_str = "=>  Available options: {" + sub_class_as_options + "}"
        parser.add_argument(
            "--frontend",
            type=str,
            help=textwrap.dedent(
                f"""\
                Optionally specify which frontend to use using the class name.
                {sub_classes_str}
                """
            ),
            metavar="",
        )
        parser.add_argument(
            "--frontend-syntax",
            action="store_true",
            help="Show available commands for the GUI.",
        )
        parser.add_argument(
            "--frontend-syntax-full",
            action="store_true",
            help="Show available commands for the GUI and shows available value-types.",
        )

    def _add_log_arguments(
        self, parser, abbrevation="", logger_name="", display_name=""
    ):
        group = parser.add_argument_group(display_name + "logger")
        group.add_argument(
            "--" + display_name + "log-disable-shell",
            action="store_true",
            help="Disable shell logging",
        )
        group.add_argument(
            "--" + display_name + "log-enable-file",
            action="store_true",
            help="Disable file logging",
        )
        group.add_argument(
            "--" + display_name + "logger-name",
            type=str,
            help="Set logger name",
            metavar="",
            default=logger_name,
        )
        group.add_argument(
            "--" + display_name + "log-level",
            type=str,
            help="Log level",
            metavar="",
            choices=["DEBUG", "INFO", "ERROR", "WARNING"],
            default="INFO",
        )
        group.add_argument(
            "--" + display_name + "log-format-shell",
            type=str,
            help="Log format shell",
            metavar="",
            default="[" + str(abbrevation) + "] %(levelname)s: %(message)s",
        )
        group.add_argument(
            "--" + display_name + "log-format-file",
            type=str,
            help="Log format file",
            metavar="",
            default="%(levelname)s: %(message)s",
        )

    def _get_sub_classes(self, cur_class):
        sub_classes = cur_class.__subclasses__()
        recursive = []
        for sub_class in sub_classes:
            recursive.extend(self._get_sub_classes(sub_class))

        return sub_classes + recursive

    def _select_subclass_and_add_custom_arguments(
        self, parser, parent, class_name, default_class
    ):
        sub_classes = [parent] + self._get_sub_classes(parent)

        selected_class = None

        for sub_class in sub_classes:
            full_class_name = sub_class.__name__
            selected_by_default = not class_name and full_class_name == default_class
            selected = full_class_name == class_name
            if selected_by_default or selected:
                group = parser.add_argument_group(full_class_name)
                sub_class.register_options(group)

                should_show_frontend_syntax = self._show_frontend_syntax in [
                    ShowFrontendSyntaxEnum.SHOW,
                    ShowFrontendSyntaxEnum.FULL,
                ]

                if should_show_frontend_syntax and hasattr(
                    sub_class, "available_syntax"
                ):
                    print(sub_class.available_syntax(self._show_frontend_syntax))
                    sys.exit()

                selected_class = sub_class

        if not selected_class:
            raise RuntimeError(f"Invalid class name provided: {class_name}")

        return selected_class
