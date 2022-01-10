from pydantic.generics import GenericModel
from typing import TypeVar, Optional, Generic, Any

from pydantic.main import BaseModel

T = TypeVar("T")

class Response(GenericModel, Generic[T]):
    data: Optional[T] = None
    error: Any = None

    success: bool

class ErrorResponse(BaseModel):
    error_code: str
    error_desc: str
