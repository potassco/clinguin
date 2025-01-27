"""
Clinguin package - package entry point
"""

import copy
import sys
import threading
from datetime import datetime

from .client_helper import start as client_start
from .parse_input import ArgumentParser
from .server_helper import start as server_start


def args_to_dict_converter(args_dict, timestamp, name_prefix=""):
    """
    Converts the ''external-logger-config'' representation into an internal one
    """
    log_dict = {}
    log_dict["file_enabled"] = args_dict[name_prefix + "log_enable_file"]
    log_dict["shell_disabled"] = args_dict[name_prefix + "log_disable_shell"]
    log_dict["name"] = args_dict[name_prefix + "logger_name"]
    log_dict["level"] = args_dict[name_prefix + "log_level"]
    log_dict["format_shell"] = args_dict[name_prefix + "log_format_shell"]
    log_dict["format_file"] = args_dict[name_prefix + "log_format_file"]
    log_dict["timestamp"] = timestamp

    return log_dict


def main():
    """
    Main entry point into the project
    """

    parser = ArgumentParser()

    if len(sys.argv) > 1:
        process = sys.argv[1]
    else:
        process = sys.argv[0]

    args = parser.parse(process, sys.argv[1:])

    args_dict = vars(args)

    timestamp = datetime.now().strftime("%Y-%m-%d::%H:%M:%S")

    if args.process == "server":
        log_dict = args_to_dict_converter(args_dict, timestamp)

        args_copy = copy.deepcopy(args)
        args_copy.log_args = log_dict
        server = threading.Thread(target=server_start, args=[args_copy])

        server.start()

    elif args.process == "client":
        log_dict = args_to_dict_converter(args_dict, timestamp)

        args_copy = copy.deepcopy(args)
        args_copy.log_args = log_dict

        client_start(args_copy)

    elif args.process == "client-server":
        server_log_dict = args_to_dict_converter(
            args_dict, timestamp, name_prefix="server_"
        )
        args_copy = copy.deepcopy(args)
        args_copy.log_args = server_log_dict

        server = threading.Thread(target=server_start, args=[args_copy])

        server.start()

        client_log_dict = args_to_dict_converter(
            args_dict, timestamp, name_prefix="client_"
        )

        args_copy = copy.deepcopy(args)
        args_copy.log_args = client_log_dict

        client_start(args_copy)
