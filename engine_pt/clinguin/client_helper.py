from client.application.client_base import ClientBase
from utils.logger import Logger
from utils.singleton_container import SingletonContainer

def start(time_stamp):
    logger = Logger(time_stamp + "-client")
    instance = SingletonContainer(logger)
    
    client = ClientBase(instance)
    client.startUp()


