from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from app._core.config import settings


def setup_cors(app: FastAPI):
    origins = [
        settings.CLIENT_URL,
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
