from pydantic import BaseModel
from typing import Optional,Any

class DataResponse(BaseModel):
    status : int
    message: str
    payload : Optional[Any] = None
    success : Optional[bool] = True

    @classmethod
    def create(cls, message: str, payload: Optional[Any] = None, status: int = 200, success: bool = True):
        return cls(status=status, message=message, payload=payload, success=success)


    