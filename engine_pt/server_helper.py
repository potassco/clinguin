import uvicorn
import subprocess

from parse_input import ArgumentParser
from server_helper_helper import startServer

def start():
    parser = ArgumentParser()
    (logic_programs, engines) = parser.parse()


    startServer(logic_programs, engines)

 
