from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.middlewares.auth_middleware import get_user_id_from_cookie
from app._lab.controllers.lab_file_controller import LabFileController
from app._core.logger import logger
from app._core.responses import DataResponse
from app._core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

class CreateAllRequest(BaseModel):
    repo_url: str

class AskRequest(BaseModel):
    query: str

class LabFileRouter:
    def __init__(self):
        self.router = APIRouter(prefix="/api/lab-files", tags=["lab_files"])
        self.controller = LabFileController()
        self._add_routes()

    def _add_routes(self):
        @self.router.post("/all/{lab_id}")
        async def create_all_endpoint(
            lab_id: str,
            request: CreateAllRequest,
            user_id: str = Depends(get_user_id_from_cookie),
            db: AsyncSession = Depends(get_db)
        ):
            await self.controller.create_all(request.repo_url, user_id, lab_id, db)
            return DataResponse(status=200, message="Lab files created successfully")
        
        @self.router.get("/all/{lab_id}")
        async def get_all_endpoint(
            lab_id: str,
            db: AsyncSession = Depends(get_db)
        ):
            lab_files = await self.controller.get_all(lab_id, db)
            return DataResponse(status=200, message="Lab files fetched successfully", payload=lab_files)
        
        @self.router.post("/ask/{lab_id}")
        async def ask_endpoint(
            lab_id: str,
            request: AskRequest,
            db: AsyncSession = Depends(get_db)
        ):
            return await self.controller.ask(lab_id, request.query, db)
