import httpx
from typing import Optional
from app._core.config import settings

CODELLAMA_URL = settings.OLLAMA_URL
MODEL_NAME = "llama3.1:latest"

SUMMARY_ROLE = (
    "You are a helpful assistant that summarizes code snippets. "
    "Provide concise summaries that capture the essence of the code. "
    "Avoid unnecessary details. Use clear and simple language. "
    "Keep the summary brief and to the point. "
    "Highlight key functionalities and purpose. "
    "Focus on what the code does rather than how it does it."
)

async def summarize_text(text: str, client: Optional[httpx.AsyncClient] = None) -> str:
    if not text.strip():
        return "Empty input. No summary generated."

    should_close = False
    if client is None:
        client = httpx.AsyncClient(timeout=300.0)
        should_close = True

    try:
        payload = {
            "model": MODEL_NAME,
            "prompt": f"{SUMMARY_ROLE}\n\nSummarize the following text:\n\"\"\"{text}\"\"\"\n\n",
            "stream": False,
        }

        response = await client.post(CODELLAMA_URL, json=payload, headers={"Content-Type": "application/json"})
        response.raise_for_status()

        data = response.json()
        summary = data.get("response")
        summary = summary.strip()

        if not summary:
            print("Empty summary returned for text chunk.")
            return "No summary generated."

        return summary

    except httpx.TimeoutException:
        print("Request to timed out.")
        return "Error: Timeout while summarizing text."

    except httpx.RequestError as e:
        print(f"HTTP error while summarizing: {e}")
        return f"Error: {str(e)}"

    except Exception as e:
        print(f"Unexpected error during summarization: {e}")
        return f"Unexpected error: {str(e)}"

    finally:
        if should_close:
            await client.aclose()