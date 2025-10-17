import os

from dotenv import load_dotenv  # type: ignore

load_dotenv()


class Settings:
    PORT: int = int(os.getenv("PORT"))
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN")
    GITHUB_API_URL: str = os.getenv("GITHUB_API_URL")
    JWT_SECRET: str = os.getenv("JWT_SECRET")
    COOKIE_SECRET: str = os.getenv("COOKIE_SECRET")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    OLLAMA_URL: str = os.getenv("OLLAMA_URL")
    CLIENT_URL: str = os.getenv("CLIENT_URL")


settings = Settings()
