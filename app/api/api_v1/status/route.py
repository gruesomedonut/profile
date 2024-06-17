import logging

from fastapi import APIRouter

from app.schemas.status import ServiceStatusSchema

logger = logging.getLogger(__name__)


status_router = APIRouter(
    prefix="/status",
    tags=["Status"],
)


@status_router.get("/", response_model=ServiceStatusSchema)
def get() -> dict:
    logger.info("Status call executed")
    return {"message": "OK"}
