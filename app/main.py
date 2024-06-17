import uvicorn
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.cors import CORSMiddleware

from app.api.api_v1 import api_router
from app.config.config import config, get_allowed_origins

app = FastAPI(
    title="Starter Kit service",
)
allowed_origins = get_allowed_origins(config)
# standard middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

prefix_api_v1_version = "/api/v1"
app.include_router(api_router, prefix=prefix_api_v1_version)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=config.DEV_MODE, port=config.PORT)
