from pydantic import BaseModel
from typing import Optional

from certify.models.response import Response, ErrorResponse


class Token(BaseModel):
    access_token: str
    token_type: str
    session_key: Optional[str]

class TokenResponse(Response[Token]):
    error: ErrorResponse = None
    has_error: bool = False
