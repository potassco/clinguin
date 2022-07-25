import threading
import sys
import configparser
import json

from datetime import datetime

from clinguin.parse_input import ArgumentParser

from clinguin.server_helper import start as server_start
from clinguin.client_helper import start as client_start


parser = ArgumentParser()
args_dict = parser.parse()

config = configparser.ConfigParser(interpolation=None)
config.read('setup.cfg')

parsed_config = {}
parsed_config['metadata'] = {}
parsed_config['logger'] = {}

for key in config['metadata']:
    parsed_config['metadata'][str(key)] = str(config['metadata'][key])

timestamp = datetime.now().strftime("%Y-%m-%d::%H:%M:%S")
for key in config['options.logger']:
    parsed_config['logger'][str(key)] = {}
    elements = json.loads(str(config['options.logger'][str(key)]))
    for element in elements:
        parsed_config['logger'][str(key)][element] = elements[element]

    if 'timestamp' not in parsed_config['logger'][str(key)]:
        parsed_config['logger'][str(key)]['timestamp'] = timestamp

if args_dict['method'] == 'server' or args_dict['method'] == 'client-server':
    server = threading.Thread(target=server_start, args = [args_dict, parsed_config])
    server.start()

if args_dict['method'] == 'client' or args_dict['method'] == 'client-server':
    client_start(parsed_config)


