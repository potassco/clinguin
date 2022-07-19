# This is a package

from subprocess import Popen

import threading
import sys
from datetime import datetime

from .parse_input import ArgumentParser

from .server_helper import start as server_start
from .client_helper import start as client_start



def main():

    # TODO should also handle start client or start server individual, perhaps using subcommands 

    parser = ArgumentParser()
    (logic_programs, engines) = parser.parse()

    timestamp = datetime.now().strftime("%Y-%m-%d::%H:%M:%S")

    server = threading.Thread(target=server_start, args = [logic_programs, engines, timestamp])
    server.start()

    client_start(timestamp)


