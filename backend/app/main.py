from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.chat import router as chat_router
from app.core.config import get_settings


settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Application startup
    yield
    # Application shutdown


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Adaptive AI Language Tutor Backend",
    lifespan=lifespan,
)


app.include_router(
    chat_router,
    prefix="/api/v1",
)


@app.get("/health", tags=["System"])
async def health():
    return {
        "status": "ok",
        "environment": settings.app_env,
    }