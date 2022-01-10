from fastapi import FastAPI
from starlette.concurrency import run_in_threadpool
from datetime import timedelta
from certify.core.config import STORAGE_BUCKET

async def get_bucket(app: FastAPI):
    """Get bucket reference from Google Storage

    Args:
        app (FastAPI): FastAPI app context

    Returns:
        object: The bucket reference
    """

    bucket = await run_in_threadpool(app.state.storage.get_bucket, STORAGE_BUCKET)
    return bucket

async def get_certificate_blob(app: FastAPI, cert_id: str):
    """Get a blob reference to given certificate PDF

    Args:
        app (FastAPI): FastAPI app context
        cert_id (str): Certificate ID

    Returns:
        object: The blob reference
    """

    bucket = await get_bucket(app)
    return bucket.blob(f"certificates/{cert_id}.pdf")

async def get_certificate_link(app: FastAPI, cert_id: str) -> str:
    return await generate_download_signed_url_v4(app, f"certificates/{cert_id}.pdf")

async def generate_download_signed_url_v4(app: FastAPI, blob_name: str) -> str:
    """Generates a v4 signed URL for downloading a blob.

    Args:
        app (FastAPI): FastAPI app context
        bucket_name (str): Bucket name
        blob_name (str): File path / blob 

    Returns:
        str: Accessible URL to the blob
    """
    # bucket_name = 'your-bucket-name'
    # blob_name = 'your-object-name'

    bucket = await get_bucket(app)
    blob = bucket.blob(blob_name)

    url = blob.generate_signed_url(
        version="v4",
        expiration=timedelta(hours=1), # This URL is valid for 1 hr
        method="GET" # Allow GET requests using this URL.
    )

    return url
