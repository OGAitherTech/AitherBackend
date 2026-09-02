from fastapi import APIRouter

router = APIRouter(prefix="/api/updates", tags=["updates"])


@router.get("")
async def updates() -> dict[str, list[dict[str, str]]]:
    return {"updates": []}
