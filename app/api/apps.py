from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/apps", tags=["apps"])


class AppRegistration(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    version: str = Field(min_length=1, max_length=50)
    platform: str = Field(min_length=1, max_length=30)


@router.get("")
async def list_apps() -> dict[str, list[dict[str, str]]]:
    return {"apps": []}


@router.post("")
async def register_app(app: AppRegistration) -> dict[str, object]:
    return {
        "registered": False,
        "message": "App registry storage is not configured yet.",
        "app": app.model_dump(),
    }
