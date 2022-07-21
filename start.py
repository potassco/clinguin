from subprocess import Popen

import threading
import sys
from datetime import datetime

from clinguin.parse_input import ArgumentParser

from clinguin.server_helper import start as server_start
from clinguin.client_helper import start as client_start


parser = ArgumentParser()
(logic_programs, engines) = parser.parse()

timestamp = datetime.now().strftime("%Y-%m-%d::%H:%M:%S")

server = threading.Thread(target=server_start, args = [logic_programs, engines, timestamp])
server.start()

client_start(timestamp)


