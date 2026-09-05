# AitherBackend

The central backend API for Aither Tech applications.

## v2.5 shared Aither data

AitherBackend now provides the shared cloud-data layer for the Aither ecosystem. A signed-in Aither account can have a separate encrypted-by-transport JSON data snapshot for each Aither service, while the backend enforces ownership through the authenticated session.

### Shared data API

| Endpoint | Purpose |
| --- | --- |
| `GET /api/data` | Return all cloud data belonging to the signed-in account, grouped by app |
| `GET /api/data/{app_id}` | Return one app's data |
| `PUT /api/data/{app_id}` | Replace one app's data snapshot (2 MB maximum) |
| `DELETE /api/data/{app_id}` | Delete one app's cloud data |

App IDs are simple ecosystem identifiers such as `notes`, `clock`, `calculator`, `maps`, `ai`, `web`, `weather`, `apps`, and `tech`.

Only authenticated sessions can access these endpoints. Data is scoped by the authenticated user ID and is never returned to another account.

## Account foundation

AitherBackend includes persistent account/session authentication with FastAPI, SQLite, salted `scrypt` password hashing, server-side opaque sessions, and an HttpOnly `aither_session` cookie. GitHub Pages frontends use the same backend session with credentialed requests.

## Database

The default database is a local SQLite file at `./aither.db`. The database now includes `user_app_data`, keyed by `(user_id, app_id)`. Set `DATABASE_URL` to another supported SQLite URL when deploying or developing.

For production, use persistent storage so cloud data survives backend restarts.

## Security

Private provider/API secrets remain server-side. Cloud data endpoints require the Aither session cookie, enforce user ownership, and reject snapshots larger than 2 MB. Never put private provider keys into Aither frontend applications.

For production, use HTTPS, `SECURE_COOKIES=true`, `SameSite=None` for cross-site GitHub Pages sessions, and restrict `CORS_ORIGINS` to the actual Aither frontend origin(s).

## Connecting the ecosystem

Aither Dashboard reads `GET /api/data` and presents the signed-in user's synced app data in **My Data**. Aither apps use the same AitherBackend account and periodically synchronize their non-secret local application data. Sensitive-looking localStorage keys such as passwords, tokens, secrets, API keys, authorization values, and session values are intentionally excluded from cloud sync.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
fastapi dev app/main.py
```

The API is available at `http://127.0.0.1:8000` and interactive docs at `/docs`.

## Existing APIs

Authentication, health, status, AI, apps, updates, notifications, config, weather, and OpenAPI endpoints remain available alongside the shared data API.
