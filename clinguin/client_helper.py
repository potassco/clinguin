"""
Helper for the client-startup-process
"""

from clinguin.client import ClientBase
from clinguin.utils import Logger


def start(args):
    """
    Helper for the client-startup-process
    """
    Logger.setup_logger(args.log_args, process="client")

    client = ClientBase(args)
    client.start_up()
