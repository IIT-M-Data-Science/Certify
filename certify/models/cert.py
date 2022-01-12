from typing import List, Any
from pydantic import BaseModel
from pydantic.generics import GenericModel
from datetime import datetime
from certify.constants.cert import CertTemplate, CertType
from certify.models.response import ErrorResponse, Response
from certify.models.verify import Certificate

class Signature(BaseModel):
    name:str
    title: str 
    data: str

class CertificateData(BaseModel):
    name: str
    event_name: str 
    event_organizer: str
    event_date: str
    desc: str = None
    signatures: List[Signature]

class CertificateModel(BaseModel):
    id: str
    template: CertTemplate
    type: CertType
    data: CertificateData
    expires: datetime = None
    qr: str

class CertificateRequestModel(CertificateData):
    template: CertTemplate
    type: CertType
    expires: datetime = None
    signatures: List[str]

class CertificateResponse(Response[Certificate]):
    success: bool = True
    error: ErrorResponse = None

class CertificateErrorResponse(CertificateResponse):
    data: Any = None
    success: bool = False
    error: ErrorResponse