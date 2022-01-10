from fastapi import APIRouter

from certify.routes.api.v1 import cert, verify

router = APIRouter()
router.include_router(cert.router)
router.include_router(verify.router)