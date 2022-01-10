from pydantic import BaseModel
from datetime import date, datetime
from certify.models.response import Response, ErrorResponse


class Certificate(BaseModel):
    cert_url: str
    cert_id: str
    cert_date: datetime
    expires: datetime = None


class VerificationResponse(Response[Certificate]):
    error: ErrorResponse = None
    has_error: bool = False
