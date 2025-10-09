from fastapi import APIRouter
from app.utils.data_response import DataResponse
from app.core.config import Config

lab_router = APIRouter()

@lab_router.post("/store")
async def store_files():
    return DataResponse.create(
        status=200,
        message="Files stored successfully , running on port : {}".format(Config.PORT),
        payload={"file_ids": [1, 2, 3]},
        success=True
    )