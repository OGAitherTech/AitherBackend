from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Cookie, Header, HTTPException
from pydantic import BaseModel, Field

from app.api.auth import authenticated_user
from app.config import settings
from app.db import connection

router = APIRouter(prefix="/api/admin", tags=["admin"])


def require_admin(aither_session: str | None, authorization: str | None) -> dict[str, object]:
    user = authenticated_user(aither_session, authorization)
    if not user or str(user["email"]).lower() not in settings.admin_email_list:
        raise HTTPException(status_code=403, detail="Admin access required.")
    return user


class TelemetryEvent(BaseModel):
    app_id: str = Field(min_length=1, max_length=80)
    event: str = Field(min_length=1, max_length=120)
    details: dict[str, object] = Field(default_factory=dict)


@router.get("/overview")
async def overview(
    aither_session: str | None = Cookie(default=None, alias="aither_session"),
    authorization: str | None = Header(default=None),
) -> dict[str, object]:
    require_admin(aither_session, authorization)
    now = datetime.now(timezone.utc)
    since = (now - timedelta(minutes=15)).isoformat()
    with connection() as conn:
        users = conn.execute("SELECT COUNT(*) AS n FROM users").fetchone()["n"]
        verified = conn.execute("SELECT COUNT(*) AS n FROM users WHERE email_verified=1").fetchone()["n"]
        sessions = conn.execute("SELECT COUNT(*) AS n FROM sessions WHERE expires_at > ?", (now.isoformat(),)).fetchone()["n"]
        events_15m = conn.execute("SELECT COUNT(*) AS n FROM telemetry_events WHERE created_at >= ?", (since,)).fetchone()["n"]
        apps = conn.execute("SELECT app_id, COUNT(*) AS events FROM telemetry_events WHERE created_at >= ? GROUP BY app_id ORDER BY events DESC", (since,)).fetchall()
        audit = conn.execute("SELECT event, COUNT(*) AS n FROM audit_logs WHERE created_at >= ? GROUP BY event ORDER BY n DESC", (since,)).fetchall()
    return {
        "generated_at": now.isoformat(),
        "users": users,
        "verified_users": verified,
        "active_sessions": sessions,
        "events_last_15m": events_15m,
        "apps_last_15m": [{"app_id": r["app_id"], "events": r["events"]} for r in apps],
        "audit_last_15m": [{"event": r["event"], "count": r["n"]} for r in audit],
    }


@router.get("/users")
async def users(
    aither_session: str | None = Cookie(default=None, alias="aither_session"),
    authorization: str | None = Header(default=None),
) -> list[dict[str, object]]:
    require_admin(aither_session, authorization)
    with connection() as conn:
        rows = conn.execute("SELECT id,name,email,email_verified,created_at FROM users ORDER BY created_at DESC LIMIT 500").fetchall()
    return [dict(r) for r in rows]


@router.get("/activity")
async def activity(
    limit: int = 200,
    aither_session: str | None = Cookie(default=None, alias="aither_session"),
    authorization: str | None = Header(default=None),
) -> list[dict[str, object]]:
    require_admin(aither_session, authorization)
    limit = max(1, min(limit, 500))
    with connection() as conn:
        rows = conn.execute(
            "SELECT t.id,t.app_id,t.event,t.details_json,t.created_at,t.user_id,u.email "
            "FROM telemetry_events t LEFT JOIN users u ON u.id=t.user_id "
            "ORDER BY t.id DESC LIMIT ?", (limit,)
        ).fetchall()
    result = []
    for row in rows:
        try:
            details = json.loads(row["details_json"])
        except json.JSONDecodeError:
            details = {}
        result.append({"id": row["id"], "app_id": row["app_id"], "event": row["event"], "details": details, "created_at": row["created_at"], "user_email": row["email"]})
    return result


@router.post("/telemetry")
async def telemetry(
    payload: TelemetryEvent,
    aither_session: str | None = Cookie(default=None, alias="aither_session"),
    authorization: str | None = Header(default=None),
) -> dict[str, object]:
    user = authenticated_user(aither_session, authorization)
    details = json.dumps(payload.details, separators=(",", ":"))[:4000]
    with connection() as conn:
        conn.execute(
            "INSERT INTO telemetry_events(user_id,app_id,event,details_json,created_at) VALUES(?,?,?,?,?)",
            (str(user["id"]) if user else None, payload.app_id, payload.event, details, datetime.now(timezone.utc).isoformat()),
        )
    return {"recorded": True}
