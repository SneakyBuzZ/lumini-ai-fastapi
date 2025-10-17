from typing import Optional
from app._core.config import settings
import httpx
from app._core.responses import AppError
from app.lib.ai.build_prompt import build_prompt

CODELLAMA_URL = settings.OLLAMA_URL
MODEL_NAME = "llama3.1:latest"

async def ask_query(query: str, files: list[dict]) -> str:
    if not query.strip():
        raise AppError(400, "Prompt cannot be empty.")
    
    try:
        async with httpx.AsyncClient(timeout=300.0) as client:
            prompt = build_prompt(query, files)
            payload = {"model": MODEL_NAME, "prompt": prompt, "stream": False}
            response = await client.post(CODELLAMA_URL, json=payload, headers={"Content-Type": "application/json"})
            response.raise_for_status()
            data = response.json()
            answer = data.get("response", "").strip()
            if not answer:
                raise AppError(500, "Received empty answer from the AI model.")
            return answer
        
    except httpx.TimeoutException:
        raise AppError(504, "Request to CodeLlama timed out.")
    except httpx.RequestError as e:
        raise AppError(502, f"HTTP error while querying AI model: {str(e)}")
    except Exception as e:
        raise AppError(500, f"Unexpected error during AI query: {str(e)}")