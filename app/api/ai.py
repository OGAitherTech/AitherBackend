from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/ai", tags=["ai"])


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=20000)
    model: str | None = None


@router.get("/models")
async def models() -> dict[str, list[str]]:
    return {"models": []}


@router.post("/chat")
async def chat(_: ChatRequest) -> dict[str, object]:
    return {
        "success": False,
        "message": "Aither AI provider is not configured yet.",
    }
