from fastapi import FastAPI

from app.core.error_handlers import register_error_handlers
from app.routers import users as users_router
from app.routers import auth as auth_router
from app.core.logging import setup_logging
import logging

logger = logging.getLogger(__name__)

setup_logging()


app = FastAPI(title="training-hub API", version="0.1.0")
app.include_router(users_router.router, prefix="/api")
app.include_router(auth_router.router, prefix="/api")

register_error_handlers(app)

@app.get("/health")
def health():
    logger.info("Health check endpoint called")
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "Hello from Training Hub"}
