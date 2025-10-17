from rich.logging import RichHandler
import logging

def setup_logging():
    logging.basicConfig(
        level="INFO",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)]
    )
    logging.getLogger("uvicorn").handlers.clear()
    logging.getLogger("uvicorn.error").handlers.clear()
    logging.getLogger("uvicorn.access").handlers.clear()
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    print("🪶 Logging initialized with Rich formatting.")

logger = logging.getLogger("app_logger")