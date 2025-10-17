from fastapi import FastAPI
from app._core.responses import DataResponse

def greet(app: FastAPI):
    @app.get("/")
    def default():
        return DataResponse.create(
            status=200,
            message="Welcome to My Lumini Fastapi server!",
            payload={},
            success=True,
        )