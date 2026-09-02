from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/auth", tags=["auth"])


class LoginRequest(BaseModel):
    email: str = Field(min_length=3)
    password: str = Field(min_length=1)


@router.post("/login")
async def login(_: LoginRequest) -> dict[str, object]:
    return {
        "authenticated": False,
        "message": "Authentication provider is not configured yet.",
    }


@router.post("/logout")
async def logout() -> dict[str, str]:
    return {"status": "ok"}
