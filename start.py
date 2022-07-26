import threading
import sys
import configparser
import json

from datetime import datetime

from clinguin.parse_input import ArgumentParser

from clinguin.server_helper import start as server_start
from clinguin.client_helper import start as client_start


parser = ArgumentParser()
args_dict = vars(parser.parse())


config = configparser.ConfigParser(interpolation=None)
config.read('setup.cfg')

parsed_config = {}
parsed_config['metadata'] = {}
parsed_config['logger'] = {}

for key in config['metadata']:
    parsed_config['metadata'][str(key)] = str(config['metadata'][key])

timestamp = datetime.now().strftime("%Y-%m-%d::%H:%M:%S")
parsed_config['logger']['time'] = timestamp

"""
for key in config['options.logger']:
    parsed_config['logger'][str(key)] = {}
    elements = json.loads(str(config['options.logger'][str(key)]))
    for element in elements:
        parsed_config['logger'][str(key)][element] = elements[element]

    if 'timestamp' not in parsed_config['logger'][str(key)]:
        parsed_config['logger'][str(key)]['timestamp'] = timestamp
"""

if args_dict['method'] == 'server':
    log_dict = {}

    log_dict['name'] = args_dict['logger_name']
    log_dict['level'] = args_dict['log_level']
    log_dict['format_shell'] = args_dict['log_format_shell']
    log_dict['format_file'] = args_dict['log_format_file']
    log_dict['timestamp'] = timestamp



    server = threading.Thread(target=server_start, args = [args_dict, parsed_config, log_dict])
    server.start()

if args_dict['method'] == 'client':
    log_dict = {}

    log_dict['name'] = args_dict['logger_name']
    log_dict['level'] = args_dict['log_level']
    log_dict['format_shell'] = args_dict['log_format_shell']
    log_dict['format_file'] = args_dict['log_format_file']
    log_dict['timestamp'] = timestamp

    client_start(log_dict)


if args_dict['method'] == 'client-server':

    server_log_dict = {}

    server_log_dict['name'] = args_dict['server_logger_name']
    server_log_dict['level'] = args_dict['server_log_level']
    server_log_dict['format_shell'] = args_dict['server_log_format_shell']
    server_log_dict['format_file'] = args_dict['server_log_format_file']
    server_log_dict['timestamp'] = timestamp

    server = threading.Thread(target=server_start, args = [args_dict, parsed_config, server_log_dict])
    server.start()

    client_log_dict = {}

    client_log_dict['name'] = args_dict['client_logger_name']
    client_log_dict['level'] = args_dict['client_log_level']
    client_log_dict['format_shell'] = args_dict['client_log_format_shell']
    client_log_dict['format_file'] = args_dict['client_log_format_file']
    client_log_dict['timestamp'] = timestamp

    client_start(client_log_dict)

