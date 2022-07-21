from clinguin.client.application.client_base import ClientBase
from clinguin.utils.logger import Logger
from clinguin.utils.singleton_container import SingletonContainer

def start(time_stamp):
    logger = Logger(time_stamp + "-client")
    instance = SingletonContainer(logger)
    
    client = ClientBase(instance)
    client.startUp()


