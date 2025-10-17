from app._lab.services.lab_file_service import LabFileService
from sqlalchemy.ext.asyncio import AsyncSession

class LabFileController:
    async def create_all(self, repo_url: str, user_id: str, lab_id: str, db : AsyncSession):
        lab_file_service = LabFileService(db)
        await lab_file_service.create_all(repo_url, user_id, lab_id)

    async def get_all(self, lab_id: str, db : AsyncSession):
        lab_file_service = LabFileService(db)
        return await lab_file_service.get_all(lab_id)
