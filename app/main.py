import uvicorn
from fastapi import FastAPI
from app.middlewares.cors_middleware import setup_cors
from app._core.config import settings
from app._core.logger import setup_logging
from app._core.hello_server import greet
from app._core.database import lifespan
from app._lab.routes.lab_file_route import LabFileRouter
from app._lab.routes.lab_chat_route import LabChatRouter

app = FastAPI(title="My Lumini Fastapi server", lifespan=lifespan)

setup_cors(app)
setup_logging()

greet(app)

lab_file_router = LabFileRouter().router
lab_chat_router = LabChatRouter().router
app.include_router(lab_file_router)
app.include_router(lab_chat_router)


if __name__ == "__main__":
    print(f"🚀 Server running at http://localhost:{settings.PORT}")
    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.PORT, reload=True)
