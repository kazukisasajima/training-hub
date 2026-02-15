from pydantic import BaseModel
from typing import Any, Optional


class ErrorResponse(BaseModel):
    code: str
    message: str
    detail: Optional[Any] = None
    