# Standard Python
from fastapi import FastAPI, APIRouter

from pydantic import BaseModel
from typing import Sequence, Any

import uvicorn

# Self Defined
from server.presentation.endpoints_helper import call_function
from server.presentation.solver_dto import EngineDto




class Endpoints:
    def __init__(self, logic_programs, engines, name: str = "Default",) -> None:
        self.logic_programs = logic_programs
        self.engines = engines

        self.name = name
        self.router = APIRouter()
        self.router.add_api_route("/health", self.health, methods=["GET"])
        self.router.add_api_route("/", self.solver, methods=["POST"])


    async def health(self):
        return {"version" : "0"}

    async def solver(self, engine:EngineDto):
        result = call_function(self.engines, engine.function, engine.arguments, {})
        return {"message" : result}



