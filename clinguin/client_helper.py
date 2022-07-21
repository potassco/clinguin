from clinguin.client.application.client_base import ClientBase
from clinguin.utils.logger import Logger
from clinguin.utils.singleton_container import SingletonContainer

def start(parsed_config):
    logger = Logger(parsed_config['timestamp'] + "-client")
    instance = SingletonContainer(logger)
    
    client = ClientBase(instance)
    client.startUp()


