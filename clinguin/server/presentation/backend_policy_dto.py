from pydantic import BaseModel
from typing import Sequence, Any


class BackendPolicyDto(BaseModel):
    function: str
