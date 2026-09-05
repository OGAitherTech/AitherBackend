from __future__ import annotations

import hashlib
import hmac
import secrets
import uuid
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Cookie, Header, HTTPException, Response
from pydantic import BaseModel, Field

from app.config import settings
from app.db import connection

router = APIRouter(prefix="/api/auth", tags=["auth"])
SESSION_COOKIE = "aither_session"


def now() -> datetime:
    return datetime.now(timezone.utc)


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.scrypt(password.encode(), salt=salt, n=16384, r=8, p=1)
    return f"scrypt${salt.hex()}${digest.hex()}"


def verify_password(password: str, encoded: str) -> bool:
    try:
        _, salt_hex, digest_hex = encoded.split("$", 2)
        salt = bytes.fromhex(salt_hex)
        expected = bytes.fromhex(digest_hex)
        actual = hashlib.scrypt(password.encode(), salt=salt, n=16384, r=8, p=1)
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError):
        return False


def token_hash(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def create_session(user_id: str) -> str:
    raw = secrets.token_urlsafe(48)
    created = now()
    expires = created + timedelta(hours=settings.session_ttl_hours)
    with connection() as conn:
        conn.execute(
            "INSERT INTO sessions(token_hash,user_id,created_at,expires_at) VALUES(?,?,?,?)",
            (token_hash(raw), user_id, created.isoformat(), expires.isoformat()),
        )
        conn.execute(
            "INSERT INTO audit_logs(user_id,event,created_at) VALUES(?,?,?)",
            (user_id, "login", created.isoformat()),
        )
    return raw


def set_session_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        SESSION_COOKIE,
        token,
        httponly=True,
        secure=settings.secure_cookies,
        samesite=settings.session_cookie_samesite,
        max_age=settings.session_ttl_hours * 3600,
        path="/",
    )


def bearer_token(authorization: str | None) -> str | None:
    if not authorization:
        return None
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token.strip():
        return None
    return token.strip()


def session_token(aither_session: str | None, authorization: str | None) -> str | None:
    return bearer_token(authorization) or aither_session


def authenticated_user(aither_session: str | None, authorization: str | None) -> dict[str, object] | None:
    token = session_token(aither_session, authorization)
    if not token:
        return None
    with connection() as conn:
        row = conn.execute(
            "SELECT u.id,u.name,u.email,u.email_verified,s.expires_at FROM sessions s JOIN users u ON u.id=s.user_id WHERE s.token_hash = ?",
            (token_hash(token),),
        ).fetchone()
    if not row or datetime.fromisoformat(row["expires_at"]) <= now():
        return None
    return {"id": row["id"], "name": row["name"], "email": row["email"], "email_verified": bool(row["email_verified"])}


class RegisterRequest(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    email: str = Field(min_length=3, max_length=320)
    password: str = Field(min_length=8, max_length=200)


class LoginRequest(BaseModel):
    email: str = Field(min_length=3, max_length=320)
    password: str = Field(min_length=1, max_length=200)


@router.post("/register", status_code=201)
async def register(payload: RegisterRequest, response: Response) -> dict[str, object]:
    email = payload.email.strip().lower()
    with connection() as conn:
        if conn.execute("SELECT 1 FROM users WHERE email = ?", (email,)).fetchone():
            raise HTTPException(status_code=409, detail="An account with this email already exists.")
        user_id = str(uuid.uuid4())
        created = now().isoformat()
        conn.execute(
            "INSERT INTO users(id,name,email,password_hash,created_at) VALUES(?,?,?,?,?)",
            (user_id, payload.name.strip(), email, hash_password(payload.password), created),
        )
        conn.execute(
            "INSERT INTO audit_logs(user_id,event,created_at) VALUES(?,?,?)",
            (user_id, "account_created", created),
        )
    session_token_value = create_session(user_id)
    set_session_cookie(response, session_token_value)
    return {"authenticated": True, "session_token": session_token_value, "user": {"id": user_id, "name": payload.name.strip(), "email": email, "email_verified": False}}


@router.post("/login")
async def login(payload: LoginRequest, response: Response) -> dict[str, object]:
    email = payload.email.strip().lower()
    with connection() as conn:
        row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    if not row or not verify_password(payload.password, row["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password.")
    session_token_value = create_session(row["id"])
    set_session_cookie(response, session_token_value)
    return {"authenticated": True, "session_token": session_token_value, "user": {"id": row["id"], "name": row["name"], "email": row["email"], "email_verified": bool(row["email_verified"])}}


@router.post("/logout")
async def logout(response: Response, aither_session: str | None = Cookie(default=None, alias=SESSION_COOKIE), authorization: str | None = Header(default=None)) -> dict[str, str]:
    token = session_token(aither_session, authorization)
    if token:
        with connection() as conn:
            conn.execute("DELETE FROM sessions WHERE token_hash = ?", (token_hash(token),))
    response.delete_cookie(SESSION_COOKIE, path="/")
    return {"status": "ok"}


@router.get("/session")
async def session(aither_session: str | None = Cookie(default=None, alias=SESSION_COOKIE), authorization: str | None = Header(default=None)) -> dict[str, object]:
    user = authenticated_user(aither_session, authorization)
    return {"authenticated": bool(user), "user": user}
