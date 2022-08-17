# Standard Python
from fastapi import FastAPI, APIRouter

import logging
import clingo

from pydantic import BaseModel
from typing import Sequence, Any

from importlib.metadata import metadata

# Self Defined
from .endpoints_helper import callFunction
from .backend_policy_dto import BackendPolicyDto

from clinguin.utils import Logger

class Endpoints:
    def __init__(self, args) -> None:
        Logger.setupLogger(args.log_args)
        self._logger = logging.getLogger(args.log_args['name'])

        self.router = APIRouter()

        # Definition of endpoints
        self.router.add_api_route("/health", self.health, methods=["GET"])
        self.router.add_api_route("/", self.standardExecutor, methods=["GET"])
        self.router.add_api_route("/backend", self.policyExecutor, methods=["POST"])

        self._backend = []
        self._backend.append(args.backend(args))

    async def health(self):

        cuin = metadata('clinguin')
        return {
            "name": cuin["name"],
            "version": cuin["version"],
            "description": cuin["summary"]
        }

    async def standardExecutor(self):
        return self._backend[0].get()

    async def policyExecutor(self, backend_call_string: BackendPolicyDto):
        self._logger.debug("Got endpoint")
        symbol = clingo.parse_term(backend_call_string.function)
        function_name = symbol.name
        function_arguments = (
            list(map(lambda symb: str(symb), symbol.arguments)))

        self._logger.debug("Will call")
        result = callFunction(
            self._backend,
            function_name,
            function_arguments,
            {})
        return result
