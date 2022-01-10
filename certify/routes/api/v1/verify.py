from os import stat
from fastapi import APIRouter, Path, FastAPI, Response, Depends, status
from fastapi.exceptions import RequestValidationError
from pydantic.error_wrappers import ErrorWrapper
from certify.models.response import ErrorResponse
from certify.models.verify import VerificationResponse, Certificate
from certify.models.cert import CertificateModel
from certify.utils.storage import get_certificate_blob, get_certificate_link

router = APIRouter(prefix="/verify")


async def verify_cert_id(
    cert_id: str = Path(..., title="Certificarte ID", description="ID of certificate to verify")
) -> str:
    cert_id = cert_id.strip()

    if not cert_id.isalnum():
        raise RequestValidationError([ErrorWrapper(ValueError("Invalid cert id"), ("cert_id", ))])

    return cert_id

@router.get("{cert_id}")
async def certificate_verify(
    app: FastAPI,
    response: Response,
    cert_id: str = Depends(verify_cert_id)
) -> VerificationResponse:
    """Verfication endpoint for given certificate id, and returns a URL to download a PDF of the certificate"""

    db = app.state.db
    doc = await db.collection("certificates").document(cert_id).get()

    if not doc.exists:
        response.status_code = status.HTTP_404_NOT_FOUND
        return VerificationResponse(
            success=False,
            error=ErrorResponse(
                error_code="verify.fail",
                error_desc="Certificate with given id not found"
            )
        )

    try:
        certificate = CertificateModel(id=doc.id, **doc.to_dict())
    except:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return VerificationResponse(
            success=False,
            error=ErrorResponse(
                error_code="cert.fail",
                error_desc="Invalid certificate"
            )
        )

    cert = await get_certificate_blob(app, doc.id)
    if not cert.exists():
        # generate cert
        pass
    
    cert_url = await get_certificate_link(app, doc.id)
    
    return VerificationResponse(
        data = Certificate(
            cert_id=doc.id,
            cert_url=cert_url,
            cert_date=doc.create_time,
            expires=certificate.expires
        ),
        success=True
    )
    