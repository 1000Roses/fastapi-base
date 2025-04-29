from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar('T')

class BaseResponse(BaseModel, Generic[T]):
    status: int
    msg: str
    detail: Optional[T] = None

    @classmethod
    def response(cls, status: int, msg: str, detail: Optional[T] = None) -> 'BaseResponse[T]':
        return cls(status=status, msg=msg, detail=detail)
