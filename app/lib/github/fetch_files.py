import asyncio
import httpx
from typing import List, Dict
from app._core.config import settings
from app._core.responses import AppError

MAX_CONCURRENCY = 20

HEADERS = {
    "Accept": "application/vnd.github.v3+json",
}

if settings.GITHUB_TOKEN:
    HEADERS["Authorization"] = f"Bearer {settings.GITHUB_TOKEN}"

async def fetch_file_retry(client, url, retries=3):
    for i in range(retries):
        try:
            resp = await client.get(url, timeout=30.0)
            if resp.status_code == 403 and "X-RateLimit-Remaining" in resp.headers:
                await asyncio.sleep(5)
                continue
            resp.raise_for_status()
            return resp
        except httpx.RequestError:
            if i == retries - 1:
                raise
            await asyncio.sleep(1.5 * (i + 1))

async def fetch_repo_tree(owner: str, repo: str, branch: str = "main") -> List[Dict]:
    tree_url = f"{settings.GITHUB_API_URL}/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
    tree = []
    async with httpx.AsyncClient(headers=HEADERS) as client:
        response = await fetch_file_retry(client, tree_url)
        data = response.json()
        if "tree" in data:
            tree = [item for item in data["tree"] if item["type"] == "blob"]
        if not tree:
            raise AppError(status_code=404, message="No files found in the repository.")
    return tree

BINARY_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "bmp", "tiff", "ico",
                     "mp4", "mp3", "avi", "mov", "wmv", "flv",
                     "pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx",
                     "zip", "rar", "7z", "tar", "gz",
                     "exe", "dll", "bin", "pyc" , "class", "iml","jar"}

async def fetch_file_contents(owner: str, repo: str, files: List[Dict], branch: str = "main") -> List[Dict]:
    sem = asyncio.Semaphore(MAX_CONCURRENCY)
    results = []

    async with httpx.AsyncClient() as client:

        async def fetch_file(item):
            file_name = item['path'].split('/')[-1]
            file_extension = file_name.split('.')[-1] if '.' in file_name else ''

            if file_extension in BINARY_EXTENSIONS:
                results.append({"path": item["path"], "content": ""})
                return

            async with sem:
                raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{item['path']}"
                try:
                    response = await fetch_file_retry(client, raw_url)
                    results.append({"path": item["path"], "content": response.text})
                except Exception as e:
                    results.append({"path": item["path"], "content": f"ERROR: {str(e)}"})

        await asyncio.gather(*(fetch_file(f) for f in files))

    return results