# Standard Python
from fastapi import FastAPI, APIRouter

import logging
import clingo

from pydantic import BaseModel
from typing import Sequence, Any

from importlib.metadata import metadata

# Self Defined
from .endpoints_helper import EndpointsHelper
from .backend_policy_dto import BackendPolicyDto

from clinguin.utils import Logger

class Endpoints:
    def __init__(self, args) -> None:
        Logger.setupLogger(args.log_args, process = "server")
        self._logger = logging.getLogger(args.log_args['name'])

        self.router = APIRouter()

        # Definition of endpoints
        self.router.add_api_route("/health", self.health, methods=["GET"])
        self.router.add_api_route("/", self.standardExecutor, methods=["GET"])
        self.router.add_api_route("/backend", self.policyExecutor, methods=["POST"])

        self._backend = args.backend(args)

    async def health(self):
        self._logger.info(f"--> Health")
        cuin = metadata('clinguin')
        return {
            "name": cuin["name"],
            "version": cuin["version"],
            "description": cuin["summary"]
        }

    async def standardExecutor(self):
        self._logger.info(f"--> {self._backend.__class__.__name__}:   get()")
        return self._backend.get()

    async def policyExecutor(self, backend_call_string: BackendPolicyDto):
        self._logger.debug("Got endpoint")
        symbol = clingo.parse_term(backend_call_string.function)
        function_name = symbol.name
        function_arguments = (
            list(map(lambda symb: str(symb), symbol.arguments)))

        call_args = ",".join(function_arguments)
        self._logger.info(f"--> {self._backend.__class__.__name__}:   {function_name}({call_args})")

        result = EndpointsHelper.callFunction(
            self._backend,
            function_name,
            function_arguments,
            {})
        return result
