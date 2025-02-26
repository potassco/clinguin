"""
The command line parser for the project.
"""

import importlib
import os
import re

from argparse import ArgumentParser, _SubParsersAction
import sys
from typing import Any, Optional, cast, Dict, Set, List, Type

from rich_argparse import ArgumentDefaultsRichHelpFormatter
from rich.text import Text

from . import logging
from ..server.backends.clingo_backend import ClingoBackend

__all__ = ["get_parser"]

ascii_art_clinguin = Text(
    r"""
         _   _                           _
   ___  | | (_)  _ __     __ _   _   _  (_)  _ __
  / __| | | | | | '_ \   / _` | | | | | | | | '_ \
 | (__  | | | | | | | | | (_| | | |_| | | | | | | |
  \___| |_| |_| |_| |_|  \__, |  \__,_| |_| |_| |_|
                         |___/
    """,
    no_wrap=True,
    justify="left",
)

ascii_art_server = Text(
    r"""
         __   ___  __        ___  __
        /__` |__  |__) \  / |__  |__)
        .__/ |___ |  \  \/  |___ |  \
    """,
    no_wrap=True,
    justify="left",
)

ascii_art_client = Text(
    r"""
         __          ___      ___
        /  ` |    | |__  |\ |  |
        \__, |___ | |___ | \|  |
    """,
    no_wrap=True,
    justify="left",
)

VERSION = importlib.metadata.version("clinguin")


def add_logger(parser: ArgumentParser) -> None:
    """
    Add the log level argument to the parser.
    Args:
        parser (ArgumentParser): The parser to add the argument to.
    """

    def get_level(levels: list[tuple[str, int]], name: str) -> Optional[int]:
        for key, val in levels:
            if key == name:
                return val
        return None  # nocoverage

    levels = [
        ("error", logging.ERROR),
        ("warning", logging.WARNING),
        ("info", logging.INFO),
        ("debug", logging.DEBUG),
    ]
    parser.add_argument(
        "--log",
        default="warning",
        choices=[val for _, val in levels],
        metavar=f"{{{','.join(key for key, _ in levels)}}}",
        help="Set log level",
        type=cast(Any, lambda name: get_level(levels, name)),
    )


def get_parser() -> ArgumentParser:
    """
    Return the parser for command line options.
    """
    parser = ArgumentParser(
        description=ascii_art_clinguin + "\n🚀 Clinguin CLI - Start the server or client."
        "\nUse: clinguin server or clinguin client",  # type: ignore
        formatter_class=ArgumentDefaultsRichHelpFormatter,
    )

    parser.add_argument("--version", "-v", action="version", version=f"%(prog)s {VERSION}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    setup_server_parser(subparsers)
    setup_client_parser(subparsers)
    return parser


# ----------------- Client -----------------


def setup_client_parser(subparsers: _SubParsersAction) -> None:  # type: ignore
    """
    Setup the parser for the client command.
    Args:
        subparsers (_SubParsersAction): The subparsers to add the client command to.
    """
    parser: ArgumentParser = subparsers.add_parser(
        "client",
        description=ascii_art_clinguin
        + ascii_art_client
        + "\n🚀 Start the client for clinguin.\
        \n It will run Angular to render the UI and react to events.",  # type: ignore
        help="Start the client",
        formatter_class=ArgumentDefaultsRichHelpFormatter,
    )
    add_logger(parser)
    parser.add_argument(
        "--port",
        type=int,
        default=8001,
        metavar="",
        help="Port to serve the client",
    )

    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        metavar="",
        help="Host to bind the client to. Use 0.0.0.0 for external access.",
    )

    parser.add_argument(
        "--server-url",
        type=str,
        default="http://127.0.0.1:8000",
        metavar="",
        help="Full URL of the Clinguin Server to connect to.",
    )

    parser.add_argument(
        "--build",
        action="store_true",
        help="Rebuild the Angular frontend before serving. Requires installing Angular CLI.",
    )

    parser.add_argument(
        "--custom-path",
        type=str,
        metavar="",
        help="Path to custom frontend files to include before building.",
    )


# ----------------- Server -----------------


def get_default_backend_path() -> str:
    """
    Get the absolute path to the installed clinguin/server/backends directory.

    Returns:
        str: The full absolute path to the backend directory.
    """
    with importlib.resources.path("clinguin.server", "backends") as backend_path:
        return str(backend_path)


def get_backend_from_sysargv():
    """Extracts the backend from sys.argv manually."""
    if "--backend" in sys.argv:
        index = sys.argv.index("--backend")
        if index + 1 < len(sys.argv):  # Ensure there's a value after --backend
            return sys.argv[index + 1]
    return "ClingoBackend"  # Default backend if not specified


def find_backend_classes(directories: List[str]) -> Dict[str, str]:
    """
    Scan multiple directories for Python files and extract backend class names that inherit from ClingoBackend
    (directly or indirectly), including ClingoBackend itself, using regex.

    Arguments:
        directories (List[str]): A list of directories containing backend Python modules.

    Returns:
        Dict[str, str]: A dictionary mapping backend class names to their file paths.
    """
    backend_classes = {}

    class_pattern = re.compile(r"class\s+([A-Za-z_][A-Za-z0-9_]*)\s*(?:\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\))?\s*:")

    class_hierarchy = {}  # Maps class names to their parent class (if any)
    class_files = {}  # Maps class names to their file paths

    for directory in directories:
        if not os.path.isdir(directory):
            raise FileNotFoundError(f"Directory not found: {directory}")

        for filename in os.listdir(directory):
            if filename.endswith(".py") and filename != "__init__.py":
                module_path = os.path.join(directory, filename)

                with open(module_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Find all class definitions and their direct parents
                matches = class_pattern.findall(content)
                for class_name, parent_class in matches:
                    if class_name not in class_files:
                        class_hierarchy[class_name] = parent_class if parent_class else None
                        class_files[class_name] = module_path

    def is_subclass_of_clingo_backend(cls: str, visited: Set[str]) -> bool:
        """Recursively checks if a class inherits from ClingoBackend or is ClingoBackend itself."""
        if cls in visited:
            return False
        visited.add(cls)

        if cls == "ClingoBackend":
            return True
        parent = class_hierarchy.get(cls)
        if parent and is_subclass_of_clingo_backend(parent, visited):
            return True
        return False

    for class_name in class_hierarchy.keys():
        if is_subclass_of_clingo_backend(class_name, set()):
            backend_classes[class_name] = class_files[class_name]

    return backend_classes


def lazy_import_backend(class_name: str, backends_dict: Dict[str, str]) -> Type[ClingoBackend]:
    """
    Lazily imports the selected backend class when needed.

    Arguments:
        class_name (str): The name of the backend class to import.
        backends_dict (Dict[str, str]): A dictionary mapping backend class names to file paths.

    Returns:
        Type[ClingoBackend]: The imported backend class.

    Raises:
        ImportError: If the backend class cannot be found.
    """
    if class_name == "ClingoBackend":
        return ClingoBackend

    module_path = backends_dict.get(class_name)
    if not module_path:
        raise ImportError(f"Backend class '{class_name}' not found.")

    module_name = os.path.basename(module_path).replace(".py", "")

    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        try:
            spec.loader.exec_module(module)
        except ModuleNotFoundError as e:
            print(
                logging.colored(
                    f"Error loading backend module '{module_name}'. Make sure all required packages are imported. For default backends provided in the clinguin package, please follow the documentation to install the dependencies automatically using pip.",
                    "RED",
                )
            )
            raise e

        backend_class = getattr(module, class_name, None)
        if isinstance(backend_class, type) and issubclass(backend_class, ClingoBackend):
            return backend_class
        else:
            raise ImportError(f"Backend class '{class_name}' was found but is not a subclass of ClingoBackend.")

    raise ImportError(f"Backend class '{class_name}' was found but could not be loaded.")


def setup_server_parser(subparsers: _SubParsersAction) -> None:  # type: ignore
    """
    Setup the parser for the server command.
    Args:
        subparsers (_SubParsersAction): The subparsers to add the server command to.
    """
    parser: ArgumentParser = subparsers.add_parser(
        "server",
        description=ascii_art_clinguin
        + ascii_art_server
        + "\n🚀 Start the server for clinguin.\
        \n It will use the domain encodings to reason and the ui encodings to define the UI.",  # type: ignore
        help="Start the server",
        formatter_class=ArgumentDefaultsRichHelpFormatter,
    )
    add_logger(parser)

    default_backend_dir = get_default_backend_path()
    user_backend_dir = "./docs"  # Example user-provided path

    available_backends = find_backend_classes([default_backend_dir, user_backend_dir])

    parser.add_argument(
        "--multi",
        action="store_true",
        help="Enable multiple backend instances per client connection.",
    )

    parser.add_argument(
        "--backend",
        type=str,
        metavar=f"{{{','.join(available_backends.keys())}}}",
        help="Specify the backend class name to use.",
        default="ClingoBackend",
    )

    parser.add_argument(
        "--custom-classes",
        type=str,
        metavar="",
        help="Path to a directory containing custom backend classes.",
    )

    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        metavar="",
        help="Set the server port.",
    )

    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",  # Default to localhost
        metavar="",
        help="Specify the server host. Use 0.0.0.0 for external access.",
    )

    selected_backend_name = get_backend_from_sysargv()
    backend = lazy_import_backend(selected_backend_name, available_backends)

    group = parser.add_argument_group(
        selected_backend_name, description=f"Options registered by the selected backend: '{selected_backend_name}'."
    )
    group.title = selected_backend_name
    backend.register_options(group)
    parser.set_defaults(backend=backend)
