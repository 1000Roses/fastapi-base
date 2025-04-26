from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar('T')

class BaseResponse(BaseModel, Generic[T]):
    status: int
    msg: str
    detail: Optional[T] = None

    @classmethod
    def success(cls, detail: Optional[T] = None, msg: str = "Success") -> 'BaseResponse[T]':
        return cls(status=200, msg=msg, detail=detail)

    @classmethod
    def error(cls, status: int, msg: str, detail: Optional[T] = None) -> 'BaseResponse[T]':
        return cls(status=status, msg=msg, detail=detail) 