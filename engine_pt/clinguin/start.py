from subprocess import Popen

import threading
import sys

from parse_input import ArgumentParser

from server_helper import start as server_start
from client_helper import start as client_start

parser = ArgumentParser()
(logic_programs, engines) = parser.parse()

server = threading.Thread(target=server_start, args = [logic_programs, engines])
server.start()

client_start()


