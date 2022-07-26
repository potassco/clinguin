# This is a package
import copy
from re import X
from subprocess import Popen
import configparser

import threading
import sys
from datetime import datetime
from turtle import back

from .parse_input import ArgumentParser

from .server_helper import start as server_start
from .client_helper import start as client_start



def main():

    parser = ArgumentParser()
    args = parser.parse()
    args_dict = vars(args)

    config = configparser.ConfigParser(interpolation=None)
    config.read('setup.cfg')

    parsed_config = {}
    parsed_config['metadata'] = {}

    timestamp = datetime.now().strftime("%Y-%m-%d::%H:%M:%S")

    for key in config['metadata']:
        parsed_config['metadata'][str(key)] = str(config['metadata'][key])

    if args.process == 'server':
        log_dict = {}

        log_dict['name'] = args_dict['logger_name']
        log_dict['level'] = args_dict['log_level']
        log_dict['format_shell'] = args_dict['log_format_shell']
        log_dict['format_file'] = args_dict['log_format_file']
        log_dict['timestamp'] = timestamp

        args_copy = copy.deepcopy(args)
        args_copy.log_args= log_dict

        server = threading.Thread(target=server_start, args = [args_copy,parsed_config])
        server.start()

    if args.process == 'client':
        log_dict = {}

        log_dict['name'] = args_dict['logger_name']
        log_dict['level'] = args_dict['log_level']
        log_dict['format_shell'] = args_dict['log_format_shell']
        log_dict['format_file'] = args_dict['log_format_file']
        log_dict['timestamp'] = timestamp

        args_copy = copy.deepcopy(args)
        args_copy.log_args= log_dict

        client_start(args_copy)

    if args.process == 'client-server':
        server_log_dict = {}

        server_log_dict['name'] = args_dict['server_logger_name']
        server_log_dict['level'] = args_dict['server_log_level']
        server_log_dict['format_shell'] = args_dict['server_log_format_shell']
        server_log_dict['format_file'] = args_dict['server_log_format_file']
        server_log_dict['timestamp'] = timestamp

        args_copy = copy.deepcopy(args)
        args_copy.log_args= server_log_dict

        server = threading.Thread(target=server_start, args = [args_copy,parsed_config])
        server.start()


        client_log_dict = {}

        client_log_dict['name'] = args_dict['client_logger_name']
        client_log_dict['level'] = args_dict['client_log_level']
        client_log_dict['format_shell'] = args_dict['client_log_format_shell']
        client_log_dict['format_file'] = args_dict['client_log_format_file']
        client_log_dict['timestamp'] = timestamp

        args_copy = copy.deepcopy(args)
        args_copy.log_args= client_log_dict

        client_start(args_copy)

