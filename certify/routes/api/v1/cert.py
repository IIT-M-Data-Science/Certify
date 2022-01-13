from fastapi import APIRouter, Response, Request, Depends, status
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from starlette.concurrency import run_in_threadpool
from pydantic.error_wrappers import ErrorWrapper
from certify.constants.scope import Scope
from certify.models.cert import CertificateData, CertificateModel, CertificateResponse, CertificateErrorResponse, CertificateRequestModel
from certify.models.verify import Certificate
from certify.models.token import OAuthTokenError
from certify.utils import cert
from certify.utils.auth import require_oauth_scopes
from certify.utils.cert import generate_cert_qr, generate_certificate, get_signatures
from certify.utils.pdf import certify_pdf
from certify.utils.storage import get_certificate_blob
from datetime import date, datetime

router = APIRouter(prefix="/cert")


@router.post("/add", response_model=CertificateResponse, 
    responses={status.HTTP_401_UNAUTHORIZED: {'model': OAuthTokenError}, status.HTTP_500_INTERNAL_SERVER_ERROR: {'model': CertificateErrorResponse}},
    dependencies=[require_oauth_scopes(Scope.CreateCert)]
)
async def certificate_verify(
    request: Request,
    response: Response,
    certificate_data: CertificateRequestModel
) -> CertificateResponse:
    """[OAuth 2.0 authenticated endpoint] Create certificate with given details"""

    app = request.app
    db = app.state.db
    
    document = db.collection("certificates").document()
    
    try:
        signatures = await get_signatures(db, certificate_data.signatures)
    except:
        raise RequestValidationError([ErrorWrapper(ValueError("Invalid signature id provided"), ("data.signatures", ))])
    
    certificate = CertificateModel(
        id=document.id,
        template=certificate_data.template,
        type=certificate_data.type,
        data=CertificateData(**{**certificate_data.dict(), **dict(signatures=signatures)}),
        expires=certificate_data.expires,
        qr=""
    )
    
    certificate.qr = await generate_cert_qr(certificate)
    certificate_pdf = await generate_certificate(certificate)
    certificate_pdf = await certify_pdf(certificate_pdf)

    cert_blob = await get_certificate_blob(app, document.id)
    await run_in_threadpool(cert_blob.upload_from_file, certificate_pdf, content_type="application/pdf")
    await document.set(jsonable_encoder(certificate, exclude={"id", "qr"}))

    return CertificateResponse(
        data=Certificate(
            cert_url=f"https://verify.iitmbsc.org/{document.id}",
            cert_id=document.id,
            cert_date=datetime.now(),
            expires=certificate.expires,
        )
    )

