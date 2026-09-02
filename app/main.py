from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.status import router as status_router
from app.config import settings

app = FastAPI(
    title=settings.app_name,
    description="Central API backend for Aither Tech applications.",
    version=settings.app_version,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(status_router)
app.include_router(auth_router)


@app.get("/")
async def root() -> dict[str, str]:
    return {
        "name": settings.app_name,
        "status": "online",
        "version": settings.app_version,
        "environment": settings.environment,
        "docs": "/docs",
    }


@app.get("/api/health")
async def health() -> dict[str, object]:
    return {
        "status": "healthy",
        "service": settings.app_name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/api/version")
async def version() -> dict[str, str]:
    return {"version": settings.app_version}
