from pydantic import BaseModel
from typing import Optional

from certify.models.response import Response


class Token(BaseModel):
    access_token: str
    token_type: str
    session_key: Optional[str]


class TokenError(BaseModel):
    error_type: str
    error_code: int
    error_description: str


class TokenResponse(Response[Token]):
    error: TokenError = None
    has_error: bool = False
