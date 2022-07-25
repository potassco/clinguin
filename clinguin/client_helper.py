from clinguin.client.application.client_base import ClientBase
from clinguin.utils.logger import Logger
from clinguin.utils.singleton_container import SingletonContainer

def start(parsed_config):
    Logger.setupLogger(parsed_config['logger']['client'])
    
    client = ClientBase(parsed_config)
    client.startUp()


