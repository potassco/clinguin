"""
Module that contains the BackendPolicyDto
"""

from pydantic import BaseModel

class BackendPolicyDto(BaseModel):
    """
    Needed by the endpoints to get convert the transported json into something useful for the backend.
    """
    functions: list
