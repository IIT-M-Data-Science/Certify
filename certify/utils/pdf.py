from pydantic.types import ByteSize
import weasyprint as wp
from io import BytesIO
from PIL import Image
from base64 import b64encode


async def generate_pdf_from_template(template: str, template_tyoe: str = "basic") -> BytesIO:
    """Generate PDF binary bytes from given HTML template

    Args:
        template (str): HTML string
        template_tyoe (str, optional): Template type. Defaults to "basic".

    Returns:
        BytesIO: PDF binary
    """
    buf = BytesIO()
    
    html = wp.HTML(string=template, base_url=f"./cert/template/{template_tyoe.strip('/')}")
    html.write_pdf(buf)
    buf.seek(0)

    return buf


async def certify_pdf(pdf_data: BytesIO) -> BytesIO:
    """Certify PDF if required

    Args:
        pdf_data (BytesIO): PDF data

    Returns:
        BytesIO: PDF data
    """
    # Implement your own certification, eg: adding trust certificates.
    return pdf_data

    