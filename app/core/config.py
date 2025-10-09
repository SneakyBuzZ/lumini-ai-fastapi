import os
from dotenv import load_dotenv # type: ignore

load_dotenv()

class Config:
    PORT : int = int(os.getenv("PORT"))