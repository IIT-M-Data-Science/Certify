from typing import List
from jinja2 import Template
from io import BytesIO
import aiofiles
import qrcode
from certify.constants.cert import CertTemplate, CertType
from certify.models.cert import CertificateData, CertificateModel, Signature
from certify.utils.pdf import generate_pdf_from_template
from certify.utils.img import image_to_base64_url

async def generate_certificate(data: CertificateModel) -> BytesIO:
    """Generate Certificate PDF

    Args:
        data (CertificateModel): Certificate details

    Returns:
        BytesIO: Certificate PDF binary
    """
    await generate_certificate_description(data, update=True)

    #TODO: Get templates from database instead of local path
    cert_template = data.template.value
    async with aiofiles.open(f"./cert/template/{cert_template.strip('/')}/template.html", 'r') as f:
        template = await f.read()

    template = Template(template)
    template = template.render(cert_type=data.type, name=data.data.name.title(), cert_desc=data.data.desc, signatures=data.data.signatures, qr_code=data.qr)

    cert_pdf = await generate_pdf_from_template(template, cert_template)
    return cert_pdf

async def generate_certificate_description(data: CertificateModel, update: bool = False) -> str:
    """Generate certificate description. (TODO: Generate using a template from database)

    Args:
        data (CertificateData): Certificate data

    Returns:
        str: Description
    """
    cert_desc = data.data.desc and data.data.desc.strip()
    if not cert_desc:
        if data.type == CertType.PARTICIPATION:
            cert_desc = "for participating in {data.event_name} held by {data.event_organizer} on {data.event_date}"
        elif data.type == CertType.EXCELLENCE:
            cert_desc = "for completing {data.event_name} held by {data.event_organizer} on {data.event_date}"
        
        cert_desc = cert_desc.format(data=data.data)
        if update:
            data.data.desc = cert_desc
            
    return cert_desc    
        
async def generate_cert_qr(data: CertificateModel) -> str:
    """Generate base64 img url for given certificate data

    Args:
        data (CertificateModel): Certificate data

    Returns:
        str: base64 QR img data
    """
    url = f"https://verify.iitmbsc.org/{data.id}"
    img = qrcode.make(url)

    return await image_to_base64_url(img)


async def get_signatures(db, signatures: List[str]) -> List[Signature]:
    """Returns list of signature objects for given signature ids from database

    Args:
        db: Firestore db client
        signatures (List[str]): List of signature ids

    Returns:
        List[Signature]: List of Signature objects
    """

    signatures_col = db.collection("signatures")
    return [
        Signature(
            **(
                (await signatures_col.document(i).get()).to_dict()
            )
        )

        for i in signatures
    ]