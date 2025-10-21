from app._lab.repositories.lab_chat_repository import LabChatMessageRepository, LabChatSessionRepository
from app._core.logger import logger
from sqlalchemy.ext.asyncio import AsyncSession

class LabChatService:
    def __init__(self, db: AsyncSession):
        self.session_repository = LabChatSessionRepository(db)
        self.message_repository = LabChatMessageRepository(db)

    async def create_session(self, lab_id: str):
        session_data = {"lab_id": lab_id}
        return await self.session_repository.create(session_data)
    
    async def get_session(self, lab_id: str):
        data = await self.session_repository.get_by_lab_id(lab_id)
        no_of_sessions = len(data)

        if no_of_sessions == 0:
            logger.info(f"No chat session found for lab {lab_id}, creating a new one.")
            new_session = await self.create_session(lab_id)
            return new_session

        return data[0]

    async def create_message(self, session_id: str, user_id: str, role: str, content: str):
        message_data = {
            "session_id": session_id,
            "user_id": user_id,
            "role": role,
            "content": content,
        }
        return await self.message_repository.save(message_data)
    
    async def get_messages(self, session_id: str):
        return await self.message_repository.get_by_session(session_id)