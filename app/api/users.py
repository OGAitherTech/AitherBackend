from fastapi import APIRouter

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/me")
async def current_user() -> dict[str, object]:
    return {
        "authenticated": False,
        "user": None,
        "message": "Authentication provider is not configured yet.",
    }
