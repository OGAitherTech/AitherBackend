from fastapi import APIRouter

router = APIRouter(prefix="/api/status", tags=["status"])


@router.get("")
async def status() -> dict[str, str]:
    return {
        "status": "operational",
        "service": "AitherBackend",
    }
