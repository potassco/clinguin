# Standard Python
from fastapi import FastAPI, APIRouter

import logging
import clingo

from pydantic import BaseModel
from typing import Sequence, Any

from importlib.metadata import metadata

# Self Defined
from clinguin.server.presentation.endpoints_helper import call_function
from clinguin.server.presentation.solver_dto import SolverDto

from clinguin.utils.logger import Logger


class Endpoints:
    def __init__(self, args) -> None:
        Logger.setupLogger(args.log_args)
        self._logger = logging.getLogger(args.log_args['name'])

        self.router = APIRouter()

        # Definition of endpoints
        self.router.add_api_route("/health", self.health, methods=["GET"])
        self.router.add_api_route("/", self.standardSolver, methods=["GET"])
        self.router.add_api_route("/solver", self.solver, methods=["POST"])

        self._solver = []
        self._solver.append(args.solver(args))

    async def health(self):

        cuin = metadata('clinguin')
        return {
            "name": cuin["name"],
            "version": cuin["version"],
            "description": cuin["summary"]
        }

    async def standardSolver(self):
        return self._solver[0].get()

    async def solver(self, solver_call_string: SolverDto):

        symbol = clingo.parse_term(solver_call_string.function)
        function_name = symbol.name
        function_arguments = (
            list(map(lambda symb: str(symb), symbol.arguments)))

        result = call_function(
            self._solver,
            function_name,
            function_arguments,
            {})
        return result
