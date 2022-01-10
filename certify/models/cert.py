from typing import List
from pydantic import BaseModel
from pydantic.generics import GenericModel
from datetime import datetime
from certify.constants.cert import CertTemplate, CertType


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
