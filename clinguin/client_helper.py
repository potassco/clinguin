"""
Helper for the client-startup-process
"""
from clinguin.client.application.client_base import ClientBase
from clinguin.utils.logger import Logger

def start(args):
    """
    Helper for the client-startup-process
    """
    Logger.setupLogger(args.log_args)

    client = ClientBase(args)
    client.startUp()
