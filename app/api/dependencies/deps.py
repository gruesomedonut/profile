import logging

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from app.config.config import config

logger = logging.getLogger(__name__)
api_key_header = APIKeyHeader(name="access_token", auto_error=False)


def get_api_key(api_key_header: str = Security(api_key_header)) -> bool:
    if api_key_header == config.API_KEY:
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate API KEY"
        )
