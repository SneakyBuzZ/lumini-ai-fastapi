from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.middlewares.auth_middleware import get_user_id_from_cookie
from app._lab.controllers.lab_chat_controller import LabChatController
from app._core.responses import DataResponse
from app._core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app._core.logger import logger

class CreateMessageRequest(BaseModel):
    role : str
    content : str

class LabChatRouter:
    def __init__(self):
        self.router = APIRouter(prefix="/api/lab-chat", tags=["lab_chat"])
        self.controller = LabChatController()
        self._add_routes()

    def _add_routes(self):
        self.router.post("/sessions/{lab_id}", response_model=DataResponse)(self.create_session)
        self.router.get("/sessions/{lab_id}", response_model=DataResponse)(self.get_session)
        self.router.post("/messages/{session_id}", response_model=DataResponse)(self.create_message)
        self.router.get("/messages/{session_id}", response_model=DataResponse)(self.get_messages)

    async def create_session(self, lab_id: str, db: AsyncSession = Depends(get_db)):
        await self.controller.create_session(lab_id, db)
        return DataResponse(status=200, message="Chat session created successfully")

    async def get_session(self, lab_id: str, db: AsyncSession = Depends(get_db)):
        data = await self.controller.get_session(lab_id, db)
        return DataResponse(status=200, payload=data, message="Chat session fetched successfully")

    async def create_message(self, session_id: str, request: CreateMessageRequest,user_id: str = Depends(get_user_id_from_cookie),db: AsyncSession = Depends(get_db)):
        await self.controller.create_message(session_id,user_id, request.role, request.content, db)
        return DataResponse(status=200, message="Chat message created successfully")

    async def get_messages(self, session_id: str, db: AsyncSession = Depends(get_db)):
        data = await self.controller.get_messages(session_id, db)
        return DataResponse(status=200, payload=data, message="Chat messages fetched successfully")