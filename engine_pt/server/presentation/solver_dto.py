from pydantic import BaseModel
from typing import Sequence, Any

class EngineDto(BaseModel):
    function:str
    arguments:Sequence[str]

