from __future__ import annotations

import json
from datetime import datetime, timezone

from fastapi import APIRouter, Cookie, HTTPException, Response
from pydantic import BaseModel, Field

from app.api.auth import SESSION_COOKIE, token_hash
from app.db import connection

router = APIRouter(prefix="/api/data", tags=["data"])


def _user_id(aither_session: str | None) -> str:
    if not aither_session:
        raise HTTPException(status_code=401, detail="Authentication required.")
    with connection() as conn:
        row = conn.execute(
            "SELECT user_id, expires_at FROM sessions WHERE token_hash = ?",
            (token_hash(aither_session),),
        ).fetchone()
    if not row or datetime.fromisoformat(row["expires_at"]) <= datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Authentication required.")
    return row["user_id"]


class AppData(BaseModel):
    data: dict = Field(default_factory=dict)


@router.get("")
async def get_all_data(aither_session: str | None = Cookie(default=None, alias=SESSION_COOKIE)) -> dict[str, object]:
    user_id = _user_id(aither_session)
    with connection() as conn:
        rows = conn.execute(
            "SELECT app_id,data_json,updated_at FROM user_app_data WHERE user_id = ? ORDER BY app_id",
            (user_id,),
        ).fetchall()
    apps = {}
    for row in rows:
        try:
            apps[row["app_id"]] = {
                "data": json.loads(row["data_json"]),
                "updated_at": row["updated_at"],
            }
        except json.JSONDecodeError:
            apps[row["app_id"]] = {"data": {}, "updated_at": row["updated_at"]}
    return {"apps": apps}


@router.get("/{app_id}")
async def get_app_data(app_id: str, aither_session: str | None = Cookie(default=None, alias=SESSION_COOKIE)) -> dict[str, object]:
    user_id = _user_id(aither_session)
    with connection() as conn:
        row = conn.execute(
            "SELECT data_json,updated_at FROM user_app_data WHERE user_id = ? AND app_id = ?",
            (user_id, app_id),
        ).fetchone()
    if not row:
        return {"app_id": app_id, "data": {}, "updated_at": None}
    return {"app_id": app_id, "data": json.loads(row["data_json"]), "updated_at": row["updated_at"]}


@router.put("/{app_id}")
async def put_app_data(
    app_id: str,
    payload: AppData,
    aither_session: str | None = Cookie(default=None, alias=SESSION_COOKIE),
) -> dict[str, object]:
    user_id = _user_id(aither_session)
    if not app_id or len(app_id) > 80 or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for c in app_id):
        raise HTTPException(status_code=400, detail="Invalid app id.")
    encoded = json.dumps(payload.data, separators=(",", ":"), ensure_ascii=False)
    if len(encoded.encode("utf-8")) > 2_000_000:
        raise HTTPException(status_code=413, detail="App data is too large (2 MB maximum).")
    updated = datetime.now(timezone.utc).isoformat()
    with connection() as conn:
        conn.execute(
            "INSERT INTO user_app_data(user_id,app_id,data_json,updated_at) VALUES(?,?,?,?) "
            "ON CONFLICT(user_id,app_id) DO UPDATE SET data_json=excluded.data_json,updated_at=excluded.updated_at",
            (user_id, app_id, encoded, updated),
        )
    return {"ok": True, "app_id": app_id, "updated_at": updated}


@router.delete("/{app_id}")
async def delete_app_data(app_id: str, response: Response, aither_session: str | None = Cookie(default=None, alias=SESSION_COOKIE)) -> dict[str, object]:
    user_id = _user_id(aither_session)
    with connection() as conn:
        conn.execute("DELETE FROM user_app_data WHERE user_id = ? AND app_id = ?", (user_id, app_id))
    return {"ok": True, "app_id": app_id}
