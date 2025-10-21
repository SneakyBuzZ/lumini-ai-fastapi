from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update, delete
from sqlalchemy.exc import SQLAlchemyError
from app._core.responses import AppError
from app._core.logger import logger
from app._lab.models.lab_chat_model import lab_chat_sessions
from app._lab.models.lab_chat_model import lab_chat_messages


class LabChatSessionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict):
        try:
            stmt = (
                insert(lab_chat_sessions)
                .values(**data)
                .returning(lab_chat_sessions.c.id, lab_chat_sessions.c.lab_id)
            )
            result = await self.db.execute(stmt)
            await self.db.commit()
            return dict(result.fetchone()._mapping)
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise AppError(500, f"Failed to create chat session: {e}")

    async def get_by_id(self, session_id: str):
        try:
            stmt = select(lab_chat_sessions).where(lab_chat_sessions.c.id == session_id)
            result = await self.db.execute(stmt)
            row = result.fetchone()
            return dict(row._mapping) if row else None
        except SQLAlchemyError as e:
            logger.error(f"Error fetching chat session {session_id}: {e}")
            raise AppError(500, f"Failed to fetch chat session: {e}")

    async def get_by_lab_id(self, lab_id: str):
        try:
            stmt = select(lab_chat_sessions).where(lab_chat_sessions.c.lab_id == lab_id)
            result = await self.db.execute(stmt)
            rows = result.all()
            return [dict(row._mapping) for row in rows]
        except SQLAlchemyError as e:
            logger.error(f"Error fetching chat sessions for lab {lab_id}: {e}")
            raise AppError(500, f"Failed to fetch chat sessions for lab: {e}")

    async def delete(self, session_id: str):
        try:
            stmt = delete(lab_chat_sessions).where(lab_chat_sessions.c.id == session_id)
            await self.db.execute(stmt)
            await self.db.commit()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise AppError(500, f"Failed to delete chat session: {e}")

class LabChatMessageRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(self, data: dict):
        try:
            data['user_id'] = data.get('user_id')  if data.get('role') == 'user' else None
            stmt = (
                insert(lab_chat_messages)
                .values(**data)
                .returning(
                    lab_chat_messages.c.id,
                    lab_chat_messages.c.role,
                    lab_chat_messages.c.content,
                    lab_chat_messages.c.created_at,
                )
            )
            result = await self.db.execute(stmt)
            await self.db.commit()
            return dict(result.fetchone()._mapping)
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise AppError(500, f"Failed to save chat message: {e}")

    async def save_all(self, data_list: list[dict]):
        if not data_list:
            return []
        try:
            stmt = (
                insert(lab_chat_messages)
                .returning(
                    lab_chat_messages.c.id,
                    lab_chat_messages.c.role,
                    lab_chat_messages.c.content,
                    lab_chat_messages.c.created_at,
                )
            )
            result = await self.db.execute(stmt, data_list)
            await self.db.commit()
            return [dict(row._mapping) for row in result.all()]
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise AppError(500, f"Failed to save multiple chat messages: {e}")

    async def get_by_session(self, session_id: str):
        try:
            stmt = (
                select(lab_chat_messages)
                .where(lab_chat_messages.c.session_id == session_id)
                .order_by(lab_chat_messages.c.created_at.asc())
            )
            result = await self.db.execute(stmt)
            rows = result.all()
            return [dict(row._mapping) for row in rows]
        except SQLAlchemyError as e:
            logger.error(f"Error fetching messages for session {session_id}: {e}")
            raise AppError(500, f"Failed to fetch chat messages: {e}")

    async def delete_by_session(self, session_id: str):
        try:
            stmt = delete(lab_chat_messages).where(
                lab_chat_messages.c.session_id == session_id
            )
            await self.db.execute(stmt)
            await self.db.commit()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise AppError(500, f"Failed to delete chat messages: {e}")
