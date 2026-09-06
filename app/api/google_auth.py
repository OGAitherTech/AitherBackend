from __future__ import annotations

import secrets
import uuid

import httpx
from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel, Field

from app.api.auth import create_session, hash_password, set_session_cookie, user_payload
from app.config import settings
from app.db import connection

router = APIRouter(prefix="/api/auth", tags=["auth"])


class GoogleLoginRequest(BaseModel):
    credential: str = Field(min_length=20, max_length=10000)


@router.post("/google")
async def google_login(payload: GoogleLoginRequest, response: Response) -> dict[str, object]:
    if not settings.google_client_id:
        raise HTTPException(status_code=503, detail="Google Sign-In is not configured on the Aither Backend.")

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            result = await client.get(
                "https://oauth2.googleapis.com/tokeninfo",
                params={"id_token": payload.credential},
            )
            data = result.json()
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Could not verify the Google sign-in token.") from exc

    if result.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid Google sign-in token.")
    if data.get("aud") != settings.google_client_id:
        raise HTTPException(status_code=401, detail="Google sign-in token was issued for a different application.")
    if data.get("iss") not in {"accounts.google.com", "https://accounts.google.com"}:
        raise HTTPException(status_code=401, detail="Invalid Google token issuer.")
    if data.get("email_verified") != "true":
        raise HTTPException(status_code=403, detail="Your Google email must be verified before using it with Aither.")

    email = str(data.get("email", "")).strip().lower()
    name = str(data.get("name") or data.get("given_name") or email.split("@", 1)[0]).strip()[:80]
    if not email or "@" not in email:
        raise HTTPException(status_code=401, detail="Google did not provide a valid email address.")

    with connection() as conn:
        row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if row:
            user_id = row["id"]
            conn.execute("UPDATE users SET name = ?, email_verified = 1 WHERE id = ?", (name, user_id))
            current_name = name
        else:
            user_id = str(uuid.uuid4())
            created = __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat()
            conn.execute(
                "INSERT INTO users(id,name,email,password_hash,email_verified,created_at) VALUES(?,?,?,?,?,?)",
                (user_id, name, email, hash_password(secrets.token_urlsafe(32)), 1, created),
            )
            conn.execute(
                "INSERT INTO audit_logs(user_id,event,created_at) VALUES(?,?,?)",
                (user_id, "google_account_created", created),
            )
            current_name = name

    session_token_value = create_session(user_id)
    set_session_cookie(response, session_token_value)
    return {
        "authenticated": True,
        "session_token": session_token_value,
        "user": user_payload(user_id, current_name, email, True),
    }
