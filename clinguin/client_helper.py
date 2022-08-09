"""
Helper for the client-startup-process
"""
from clinguin.client import ClientBase
from clinguin.utils import Logger

def start(args):
    """
    Helper for the client-startup-process
    """
    Logger.setupLogger(args.log_args)

    client = ClientBase(args)
    client.startUp()
