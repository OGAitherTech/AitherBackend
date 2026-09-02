# AitherBackend

The central backend API for Aither Tech applications.

## v1 foundation

AitherBackend now has a working FastAPI foundation with:

- Health and version APIs
- Service status API
- Authentication API foundation
- Aither AI gateway foundation
- Configurable CORS
- Environment-based settings
- Interactive OpenAPI/Swagger docs
- ReDoc docs
- Docker support
- Automated API tests
- GitHub Actions CI

FastAPI provides automatic interactive API documentation at `/docs` and OpenAPI schema generation. See the official FastAPI documentation for details. citeturn0search0turn0search1

## API

| Endpoint | Purpose |
| --- | --- |
| `GET /` | Backend information |
| `GET /api/health` | Health check |
| `GET /api/version` | API version |
| `GET /api/status` | Service status |
| `POST /api/auth/login` | Authentication foundation |
| `POST /api/auth/logout` | Logout foundation |
| `GET /api/ai/models` | Available AI models |
| `POST /api/ai/chat` | AI chat gateway foundation |
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

## Security direction

Provider/API secrets should stay server-side and be supplied through environment variables or a secrets manager. Do not put private provider keys into Aither frontend apps.

## Roadmap

- Real authentication and user accounts
- Secure AI provider integration
- App registry and app configuration
- Settings synchronization
- Persistent database layer
- Token/session management
- Rate limiting
- Request logging and observability
- Production security headers
- Update/version service
- Notifications
- Expanded automated tests
