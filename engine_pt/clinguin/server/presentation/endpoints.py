# Standard Python
from fastapi import FastAPI, APIRouter

from pydantic import BaseModel
from typing import Sequence, Any

# Self Defined
from server.presentation.endpoints_helper import call_function
from server.presentation.solver_dto import SolverDto

import logging 
from utils.logger import Logger
from utils.singleton_container import SingletonContainer


class Endpoints:
    def __init__(self, logic_programs : Sequence[str], solver_classes : Sequence[Any], log_file_name:str) -> None:
        logger = Logger(log_file_name, reroute_default = True)

        self._instance = SingletonContainer(logger)
        
        self.router = APIRouter()

        # Definition of endpoints
        self.router.add_api_route("/health", self.health, methods=["GET"])
        self.router.add_api_route("/", self.solver, methods=["POST"])

        self._initSolver(logic_programs, solver_classes, self._instance)
        
        
    def _initSolver(self, logic_programs : Sequence[str], solver_classes : Sequence[Any], instance) -> None:
        self.solver = []
        self.solver.append(solver_classes[0](logic_programs, instance))


    async def health(self):
        return {"version" : "0"}

    async def solver(self, solver:SolverDto):
        splits = solver.function.split("(") 

        function = splits[0]

        rest = ""
        for i in range(1, len(splits)):
            if i == 1:
                rest = rest + splits[i]
            else:
                rest = rest + "(" + splits[i]


        arguments = []
        cur = ""
        open_brackets = 0
        for char in rest:
            if char == '(':
                open_brackets = open_brackets + 1
            elif char == ')':
                if open_brackets > 0:
                    open_brackets = open_brackets - 1
                else: # Last Character
                    arguments.append(cur)
                    break
                    
            elif char == ',' and open_brackets == 0:
                arguments.append(cur)
                cur = ""
                continue

            cur = cur + char

        result = call_function(self.solver, function, arguments, {})
        return result



