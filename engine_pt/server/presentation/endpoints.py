# Standard Python
from fastapi import FastAPI, APIRouter

from pydantic import BaseModel
from typing import Sequence, Any

import uvicorn

# Self Defined
from server.presentation.endpoints_helper import call_function
from server.presentation.solver_dto import SolverDto

class Endpoints:
    def __init__(self, logic_programs : Sequence[str], solver_classes : Sequence[Any], name: str = "Default",) -> None:
        self.name = name
        self.router = APIRouter()

        # Definition of endpoints
        self.router.add_api_route("/health", self.health, methods=["GET"])
        self.router.add_api_route("/", self.solver, methods=["POST"])

        self._initSolver(logic_programs, solver_classes)
        
        
    def _initSolver(self, logic_programs : Sequence[str], solver_classes : Sequence[Any]) -> None:
        self.solver = []
        self.solver.append(solver_classes[0](logic_programs))


    async def health(self):
        return {"version" : "0"}

    async def solver(self, solver:SolverDto):
        result = call_function(self.solver, solver.function, solver.arguments, {})
        return {"message" : result}



