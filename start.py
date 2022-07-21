from subprocess import Popen

import threading
import sys
import configparser

from datetime import datetime

from clinguin.parse_input import ArgumentParser

from clinguin.server_helper import start as server_start
from clinguin.client_helper import start as client_start


parser = ArgumentParser()
(logic_programs, engines) = parser.parse()

timestamp = datetime.now().strftime("%Y-%m-%d::%H:%M:%S")

config = configparser.ConfigParser()
config.read('setup.cfg')

parsed_config = {}
for key in config['metadata']:
    parsed_config[str(key)] = str(config['metadata'][key])
parsed_config['timestamp'] = timestamp

server = threading.Thread(target=server_start, args = [logic_programs, engines, parsed_config])
server.start()

client_start(parsed_config)

