"""
Module that contains the BackendOperationDto
"""

from typing import List, Optional

from pydantic import BaseModel


class ContextDto(BaseModel):
    """
    Optional pass to the backend, which handles the context.
    """

    key: str
    value: str


class BackendOperationDto(BaseModel):
    """
    Needed by the endpoints to get convert the transported json into something useful for the backend.
    """

    function: str
    context: Optional[List[ContextDto]] = []
