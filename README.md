# AitherBackend

The central backend API for Aither Tech applications.

## Stack

- Python 3.12+
- FastAPI
- Pydantic Settings
- Docker-ready

## API

| Endpoint | Purpose |
| --- | --- |
| `GET /` | Backend information |
| `GET /api/health` | Health check |
| `GET /api/version` | API version |
| `GET /docs` | Interactive Swagger API docs |
| `GET /redoc` | ReDoc API docs |

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
fastapi dev app/main.py
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
fastapi dev app/main.py
```

The API will be available at `http://127.0.0.1:8000` and the interactive docs at `http://127.0.0.1:8000/docs`.

## Docker

```bash
docker build -t aither-backend .
docker run --rm -p 8000:8000 aither-backend
```

## Roadmap

- Authentication and user accounts
- Aither AI gateway
- App registry and app configuration
- Secure server-side API integrations
- Settings synchronization
- Update/version service
- Notifications
- Persistent database layer
- Rate limiting and production security
- Automated tests and CI
