# This is a package

from re import X
from subprocess import Popen

import threading
import sys
from datetime import datetime
from turtle import back

from .parse_input import ArgumentParser

from .server_helper import start as server_start
from .client_helper import start as client_start



def main():

    # TODO should also handle start client or start server individual, perhaps using subcommands 

    parser = ArgumentParser()
    # server command
    # get all classes implementing clinguin back
    # for name, obj in inspect.getmembers(sys.modules[__name__]):
    #     if inspect.isclass(obj):
    #         if issubclass(obj,Evaluator):
    # for each class C 
    #     GroupParser 
    #     C._register_option(GroupParser)

    (logic_programs, engines) = parser.parse()

    timestamp = datetime.now().strftime("%Y-%m-%d::%H:%M:%S")

    server = threading.Thread(target=server_start, args = [logic_programs, engines, timestamp])
    server.start()


    client_start(timestamp)


