from pydantic import BaseModel
from typing import Sequence, Any


class SolverDto(BaseModel):
    function: str
