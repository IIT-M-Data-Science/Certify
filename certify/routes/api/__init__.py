from fastapi import APIRouter

from certify.routes.api import v1

router = APIRouter()
#router.include_router(v1.router, prefix="/v1", tags=["API v1"])