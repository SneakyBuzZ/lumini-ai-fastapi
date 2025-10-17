from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select
from app._lab.models.lab_file_model import lab_files
from sqlalchemy.exc import SQLAlchemyError
from app._core.responses import AppError
from app._core.logger import logger

class LabFileRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(self, data: dict):
        try:
            stmt = insert(lab_files).values(**data)
            await self.db.execute(stmt)
            await self.db.commit()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise AppError(500, f"Failed to save lab file: {e}")

    async def save_all(self, data_list: list[dict]):
        if not data_list:
            return
        try:
            stmt = (
                insert(lab_files)
                .returning(lab_files.c.id, lab_files.c.name, lab_files.c.path, lab_files.c.summary)
            )

            result = await self.db.execute(stmt, data_list)
            await self.db.commit()

            inserted_files = [dict(row._mapping) for row in result.all()]
            return inserted_files
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise AppError(500, f"Failed to save lab files: {e}")
        
    async def get_lab_files(self, lab_id: str):
        query = select(lab_files).where(lab_files.c.lab_id == lab_id)
        try:
            result = await self.db.execute(query)
            rows = result.all()
            files = [dict(row._mapping) for row in rows]
            return files or []
        except SQLAlchemyError as e:
            logger.error(f"Error fetching lab files for lab_id {lab_id}: {e}")

    async def get_lab_files(self, ids: list[str]):
        query = select(lab_files).where(lab_files.c.id.in_(ids))
        try:
            result = await self.db.execute(query)
            rows = result.all()
            files = [dict(row._mapping) for row in rows]
            return files or []
        except SQLAlchemyError as e:
            logger.error(f"Error fetching lab files for ids {ids}: {e}")