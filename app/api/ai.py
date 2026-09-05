from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import httpx

from app.config import settings

router = APIRouter(prefix="/api/ai", tags=["ai"])


class Message(BaseModel):
    role: str = Field(pattern="^(system|user|assistant)$")
    content: str = Field(min_length=1, max_length=20000)


class ChatRequest(BaseModel):
    messages: list[Message] = Field(min_length=1, max_length=100)
    model: str | None = None


@router.get("/models")
async def models() -> dict[str, list[str]]:
    if not settings.openrouter_api_key:
        return {"models": []}
    return {"models": [settings.ai_model]}


@router.post("/chat")
async def chat(request: ChatRequest) -> dict[str, object]:
    if not settings.openrouter_api_key:
        raise HTTPException(status_code=503, detail="Aither AI provider is not configured on AitherBackend.")

    payload = {
        "model": request.model or settings.ai_model,
        "messages": [message.model_dump() for message in request.messages],
        "temperature": settings.ai_temperature,
    }
    headers = {
        "Authorization": f"Bearer {settings.openrouter_api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": settings.app_url,
        "X-Title": "Aither AI",
    }

    try:
        async with httpx.AsyncClient(timeout=settings.ai_timeout_seconds) as client:
            response = await client.post(settings.openrouter_url, json=payload, headers=headers)
    except httpx.TimeoutException as exc:
        raise HTTPException(status_code=504, detail="Aither AI provider timed out.") from exc
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail="Could not reach the Aither AI provider.") from exc

    if response.status_code >= 400:
        try:
            error = response.json().get("error", {}).get("message", "Provider request failed")
        except Exception:
            error = "Provider request failed"
        raise HTTPException(status_code=502, detail=str(error))

    data = response.json()
    choices = data.get("choices") or []
    if not choices:
        raise HTTPException(status_code=502, detail="Aither AI provider returned no response.")

    content = choices[0].get("message", {}).get("content", "")
    if isinstance(content, list):
        content = "".join(part.get("text", "") for part in content if isinstance(part, dict))
    content = str(content).strip()
    if not content:
        raise HTTPException(status_code=502, detail="Aither AI provider returned an empty response.")

    return {
        "success": True,
        "reply": content,
        "model": data.get("model") or payload["model"],
    }
