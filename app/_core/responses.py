from typing import Any, Optional
from pydantic import BaseModel

class DataResponse(BaseModel):
    status: int
    message: str
    payload: Optional[Any] = None
    success: Optional[bool] = True

    @classmethod
    def create(
        cls,
        message: str,
        payload: Optional[Any] = None,
        status: int = 200,
        success: bool = True,
    ):
        return cls(status=status, message=message, payload=payload, success=success)


class AppError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(message)
