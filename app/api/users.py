from __future__ import annotations

from fastapi import APIRouter, Cookie

from app.api.auth import SESSION_COOKIE, token_hash
from app.db import connection

router = APIRouter(prefix="/api/users", tags=["users"])


def get_session_user(aither_session: str | None):
    if not aither_session:
        return None
    from datetime import datetime, timezone
    with connection() as conn:
        row = conn.execute("SELECT u.id,u.name,u.email,u.email_verified,s.expires_at FROM sessions s JOIN users u ON u.id=s.user_id WHERE s.token_hash=?", (token_hash(aither_session),)).fetchone()
    if not row or datetime.fromisoformat(row["expires_at"]) <= datetime.now(timezone.utc):
        return None
    return {"id":row["id"],"name":row["name"],"email":row["email"],"email_verified":bool(row["email_verified"])}


@router.get("/me")
async def current_user(aither_session: str | None = Cookie(default=None, alias=SESSION_COOKIE)) -> dict[str, object]:
    user = get_session_user(aither_session)
    return {"authenticated": bool(user), "user": user}
