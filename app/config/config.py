import os
from typing import Optional, cast

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Config(BaseSettings):
    RDS_URI: str = cast(str, os.getenv("RDS_URI"))
    ALLOWED_ORIGINS_REGISTRY: Optional[str] = cast(
        str, os.getenv("ALLOWED_ORIGINS_REGISTRY", False)
    )
    API_KEY: str = cast(str, os.getenv("API_KEY"))
    PORT: int = cast(int, os.getenv("PORT", 8000))
    # The hosts to add as trusted hosts for this API
    TRUSTED_HOSTS: list[str] = ["*"]
    DEV_MODE: bool = cast(bool, os.getenv("DEV_MODE", False))

    class Config:
        case_sensitive = False


def get_allowed_origins(config: Config) -> list:
    origins = ["*"]
    if config.ALLOWED_ORIGINS_REGISTRY:
        with open(config.ALLOWED_ORIGINS_REGISTRY, "r") as origins_file:
            origins = []
            for line in origins_file:
                origins.append(line.strip())

    return origins


config = Config()
