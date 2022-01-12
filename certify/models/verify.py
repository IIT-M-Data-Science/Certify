from typing import Any
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

class VerificationErrorResponse(VerificationResponse):
    data: Any = None
    success: bool = False
    error: ErrorResponse

class CertificateNotFound(VerificationErrorResponse):
    error: ErrorResponse = ErrorResponse(
        error_code="verify.fail",
        error_desc="Certificate with given id not found"
    )

class CertificateDataInvalid(VerificationErrorResponse):
    error: ErrorResponse = ErrorResponse(
        error_code="cert.fail",
        error_desc="Invalid certificate"
    )

