import threading
import sys
import configparser
import json

from datetime import datetime

from clinguin.parse_input import ArgumentParser

from clinguin.server_helper import start as server_start
from clinguin.client_helper import start as client_start


parser = ArgumentParser()
(logic_programs, engines) = parser.parse()


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

server = threading.Thread(target=server_start, args = [logic_programs, engines, parsed_config])
server.start()

client_start(parsed_config)
