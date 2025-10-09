from fastapi import FastAPI
from app.middlewares.cors_middleware import setup_cors
from app.routes.lab_route import lab_router
from app.utils.data_response import DataResponse

app = FastAPI(title="Lumini Fastapi server")

@app.get("/")
def default():
    return DataResponse.create(
        status=200,
        message="Welcome to My Lumini Fastapi server!",
        payload={},
        success=True
    )

    return Data

setup_cors(app)

app.include_router(lab_router, prefix="/api/lab", tags=["lab"])

