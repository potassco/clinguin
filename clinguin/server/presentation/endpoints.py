"""
Module for the Endpoints class.
"""
import logging
from importlib.metadata import metadata

from fastapi import APIRouter

import clingo

from clinguin.utils import Logger
# Self Defined
from .endpoints_helper import EndpointsHelper
from .backend_policy_dto import BackendPolicyDto


class Endpoints:
    """
    The endpoints class define the available endpoints the backend (this time backend refers to the general concept of backend, like a server backend) has. These are defined in the ''__init__'', and correspond to the three methods:

    Methods:
        health -> Json : Returns name, version and description of clinguin.
        standard_executor -> Json : Returns the default GUI representation as Json that the Backend provides.
        policy_executor -> Json : Executes a policy defined by the Json passed with the Post request.
    """
    def __init__(self, args) -> None:
        Logger.setup_logger(args.log_args, process = "server")
        self._logger = logging.getLogger(args.log_args['name'])

        self.router = APIRouter()

        # Definition of endpoints
        self.router.add_api_route("/health", self.health, methods=["GET"])
        self.router.add_api_route("/", self.standard_executor, methods=["GET"])
        self.router.add_api_route("/backend", self.policy_executor, methods=["POST"])

        self._backend = args.backend(args)

    async def health(self):
        self._logger.info("--> Health")
        cuin = metadata('clinguin')
        return {
            "name": cuin["name"],
            "version": cuin["version"],
            "description": cuin["summary"]
        }

    async def standard_executor(self):
        self._logger.info("--> %s:   get()", self._backend.__class__.__name__)
        return self._backend.get()

    async def policy_executor(self, backend_call_string: BackendPolicyDto):
        self._logger.debug("Got endpoint")
        symbol = clingo.parse_term(backend_call_string.function)
        function_name = symbol.name
        function_arguments = (
            list(map(str, symbol.arguments)))

        call_args = ",".join(function_arguments)
        self._logger.info("--> %s:   %s(%s))", self._backend.__class__.__name__, function_name, call_args)

        result = EndpointsHelper.call_function(
            self._backend,
            function_name,
            function_arguments,
            {})
        
        return result
