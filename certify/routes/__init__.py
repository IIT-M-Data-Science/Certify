from fastapi import APIRouter

from certify.routes import api

router = APIRouter()
router.include_router(api.router, prefix="/api", tags=["CertAPI"])