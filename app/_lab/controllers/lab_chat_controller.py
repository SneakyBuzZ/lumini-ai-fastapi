from sqlalchemy.ext.asyncio import AsyncSession
from app._lab.services.lab_chat_service import LabChatService
from app._core.logger import logger

class LabChatController:
    async def create_session(self, lab_id: str, db: AsyncSession):
        lab_chat_service = LabChatService(db)
        return await lab_chat_service.create_session(lab_id)
    
    async def get_session(self, lab_id: str, db: AsyncSession):
        lab_chat_service = LabChatService(db)
        return await lab_chat_service.get_session(lab_id)
    
    async def create_message(self, session_id: str, user_id: str, role: str, content: str, db: AsyncSession):
        lab_chat_service = LabChatService(db)
        logger.info(f"CREATING CHAT MESSAGE: {content}")
        return await lab_chat_service.create_message(session_id, user_id, role, content)

    async def get_messages(self, session_id: str, db: AsyncSession):
        lab_chat_service = LabChatService(db)
        return await lab_chat_service.get_messages(session_id)