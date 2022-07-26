# Standard Python
from fastapi import FastAPI, APIRouter

import logging 
import clingo

from pydantic import BaseModel
from typing import Sequence, Any

# Self Defined
from clinguin.server.presentation.endpoints_helper import call_function
from clinguin.server.presentation.solver_dto import SolverDto

from clinguin.utils.logger import Logger
from clinguin.utils.singleton_container import SingletonContainer

from clinguin.server.application.standard_solver import ClingoBackend


class Endpoints:
    def __init__(self ,args ,parsed_config, log_dict) -> None:
        Logger.setupLogger(log_dict)
        self._logger = logging.getLogger(log_dict['name'])

        self._parsed_config = parsed_config
        
        self.router = APIRouter()

        # Definition of endpoints
        self.router.add_api_route("/health", self.health, methods=["GET"])
        self.router.add_api_route("/", self.standardSolver, methods=["GET"])
        self.router.add_api_route("/solver", self.solver, methods=["POST"])

        self._solver = []
        self._solver.append(args['solver'](args, log_dict))

    async def health(self):
        return {
            "name" : self._parsed_config["metadata"]["name"],
            "version" : self._parsed_config["metadata"]["version"],
            "description" : self._parsed_config["metadata"]["description"]
            }

    async def standardSolver(self):
        return self._solver[0]._get()

    async def solver(self, solver_call_string:SolverDto):

        symbol = clingo.parse_term(solver_call_string.function)
        function_name = symbol.name
        function_arguments = (list(map(lambda symb:str(symb), symbol.arguments)))

        result = call_function(self._solver, function_name, function_arguments, {})
        return result



