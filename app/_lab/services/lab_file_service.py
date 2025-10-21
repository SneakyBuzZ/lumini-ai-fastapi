from httpx import get
from app._lab.repositories.lab_file_repository import LabFileRepository
from app.lib.github.parse_repo_url import parse_repo_url
from app.lib.github.fetch_files import fetch_repo_tree, fetch_file_contents
from app.lib.ai.chunk_file import chunk_file
from app.lib.ai.summarize_text import summarize_text
from app._core.logger import logger
from sqlalchemy.ext.asyncio import AsyncSession
from asyncio import gather
from app._core.responses import AppError
from app.lib.embeddings.qdrant import store_embeddings, get_similar_files
from app.lib.embeddings.sentence_transformer import generate_embedding
from app.lib.ai.ask_query import ask_query

class LabFileService:
    def __init__(self, db: AsyncSession):
        self.repository = LabFileRepository(db)
    
    async def create_all(self, repo_url: str, user_id: str, lab_id: str):
        owner, repo = parse_repo_url(repo_url)
        files = await self.get_github_files(owner, repo)

        if not files:
            logger.warning(f"No files to process for repo: {repo_url}")
            raise AppError(404, "No files found in the repository.")    

        summarized_files = await self.get_summarized_github_files(files)
        lab_files_data = self.get_lab_files_data(summarized_files, user_id, lab_id)

        inserted_files = await self.repository.save_all(lab_files_data)
        await store_embeddings(inserted_files, lab_id)

    async def get_all(self, lab_id: str):
        return await self.repository.get_lab_files(lab_id)

    async def ask(self, lab_id: str, query: str):
        query_embedding = generate_embedding(query)
        similar_files = await get_similar_files(query_embedding, lab_id)
        ids = [file['file_id'] for file in similar_files]
        similar_files = await self.repository.get_lab_files(ids)
        return await ask_query(query, similar_files)

    def get_lab_files_data(self, files: list[dict], user_id: str, lab_id: str):
        lab_files_data = []
        for file in files:
            lab_file = {
                "user_id": user_id,
                "lab_id": lab_id,
                "name" : file['path'].split('/')[-1],
                "path": file['path'],
                "content": file.get('content', ''),
                "summary": file.get('summary', ''),
            }
            lab_files_data.append(lab_file)
        return lab_files_data

    async def get_summarized_github_files(self, files : list[dict]) -> list[dict]:
        async def summarize_single_file(file:dict) -> dict:
            if not file.get("content"):
                file["summary"] = "No content to summarize."
                return file

            file_chunks = chunk_file(file['content'])
            summaries = await gather(*[
                summarize_text(chunk) for chunk in file_chunks
            ])

            file["summary"] = " ".join(summaries)
            return file

        summarized_files = await gather(*[
            summarize_single_file(file) for file in files
        ])
        return summarized_files

    async def get_github_files(self, owner: str, repo: str):
        tree = await fetch_repo_tree(owner, repo)
        if not tree:
            logger.warning(f"No files found in the repository {owner}/{repo}")
            return []
        
        files = await fetch_file_contents(owner,repo,tree)
        if not files:
            logger.warning(f"No files found for {owner}/{repo}")
            return []
        
        files = [dict(f) for f in files]

        return files