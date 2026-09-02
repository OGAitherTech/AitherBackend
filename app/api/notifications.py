from fastapi import APIRouter

router = APIRouter(prefix="/api/notifications", tags=["notifications"])


@router.get("")
async def notifications() -> dict[str, list[dict[str, str]]]:
    return {"notifications": []}
