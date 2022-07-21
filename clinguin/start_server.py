from server_helper import start
from parse_input import ArgumentParser

parser = ArgumentParser()
(logic_programs, engines) = parser.parse()

start(logic_programs, engines)  


