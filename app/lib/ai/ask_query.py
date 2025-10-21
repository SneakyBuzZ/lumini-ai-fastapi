import httpx
import json
from fastapi.responses import StreamingResponse
from app._core.responses import AppError
from app.lib.ai.build_prompt import build_prompt

AI_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.1:latest"

async def ask_query(query: str, files: list[dict]):
    prompt = build_prompt(query, files)

    async def stream_generator():
        try:
            async with httpx.AsyncClient(timeout=300.0) as client:
                async with client.stream("POST", AI_URL, json={
                    "model": MODEL_NAME,
                    "prompt": prompt,
                    "stream": True
                }) as response:
                    response.raise_for_status()
                    async for line in response.aiter_lines():
                        if not line.strip():
                            continue
                        try:
                            data = json.loads(line)
                            chunk = data.get("response", "")
                            for chunk in chunk:
                                yield chunk
                        except json.JSONDecodeError:
                            continue
        except Exception as e:
            yield f"\n[Error] Streaming failed: {str(e)}"

    return StreamingResponse(stream_generator(), media_type="text/plain")
