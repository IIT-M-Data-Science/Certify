from io import BytesIO
from PIL import Image
from base64 import b64encode

async def image_to_base64_url(img: Image) -> str:
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    return f"data:image/png;base64,{b64encode(buf.read()).decode()}"

