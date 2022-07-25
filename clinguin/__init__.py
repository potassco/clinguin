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

    # TODO should also handle start client or start server individual, perhaps using subcommands 

    parser = ArgumentParser()
    args = parser.parse()

    config = configparser.ConfigParser(interpolation=None)
    config.read('setup.cfg')

    parsed_config = {}
    parsed_config['metadata'] = {}

    for key in config['metadata']:
        parsed_config['metadata'][str(key)] = str(config['metadata'][key])


    log_args = {
        'timestamp':datetime.now().strftime("%Y-%m-%d::%H:%M:%S"),
        'level':args.log_level,
        'format_file':args.log_format_file,
        'format_shell':args.log_format_shell
    }

    if args.process == 'server' or args.process == 'client-server':
        args_copy = copy.deepcopy(args)
        args_copy.log_args= copy.deepcopy(log_args)
        args_copy.log_args['name']='server'
        print(args_copy)
        server = threading.Thread(target=server_start, args = [args_copy,parsed_config])
        server.start()

    if args.process == 'client' or args.process == 'client-server':
        args_copy = copy.deepcopy(args)
        args_copy.log_args= copy.deepcopy(log_args)
        args_copy.log_args['name']='client'
        client_start(args_copy)




    # parser = ArgumentParser()

    # (logic_programs, engines) = parser.parse()

    # timestamp = datetime.now().strftime("%Y-%m-%d::%H:%M:%S")

    # server = threading.Thread(target=server_start, args = [logic_programs, engines, timestamp])
    # server.start()


    # client_start(timestamp)


