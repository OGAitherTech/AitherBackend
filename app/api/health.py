from fastapi import APIRouter

from app.database import healthcheck as database_healthcheck

router = APIRouter(prefix="/api/health", tags=["health"])


@router.get("/dependencies")
async def dependencies() -> dict[str, object]:
    return {
        "status": "healthy" if await database_healthcheck() else "degraded",
        "database": "ready",
    }
