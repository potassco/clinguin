from clinguin.client.application.client_base import ClientBase
from clinguin.utils.logger import Logger
from clinguin.utils.singleton_container import SingletonContainer


def start(args):
    Logger.setupLogger(args.log_args)

    client = ClientBase(args)
    client.startUp()
