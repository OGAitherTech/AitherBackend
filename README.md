# AitherBackend

The central backend API for Aither Tech applications.

## v1 foundation

AitherBackend now has a working FastAPI foundation with:

- Health and version APIs
- Dependency health endpoint
- Service status API
- Authentication API foundation
- Aither AI gateway foundation
- Aither app registry foundation
- Update service foundation
- Configurable CORS
- Environment-based settings
- Interactive OpenAPI/Swagger docs
- ReDoc docs
- Docker support
- Render deployment configuration
- Automated API tests
- GitHub Actions CI
- Developer Makefile
- Security and contribution guides

FastAPI provides automatic interactive API documentation and OpenAPI schema generation. citeturn0search0turn0search1

## API

| Endpoint | Purpose |
| --- | --- |
| `GET /` | Backend information |
| `GET /api/health` | Health check |
| `GET /api/health/dependencies` | Dependency health |
| `GET /api/version` | API version |
| `GET /api/status` | Service status |
| `POST /api/auth/login` | Authentication foundation |
| `POST /api/auth/logout` | Logout foundation |
| `GET /api/ai/models` | Available AI models |
| `POST /api/ai/chat` | AI chat gateway foundation |
| `GET /api/apps` | Aither app registry |
| `POST /api/apps` | Register an app |
| `GET /api/updates` | Available app updates |
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
- App registry database storage
- Settings synchronization
- Persistent database layer
- Token/session management
- Rate limiting
- Request logging and observability
- Production security headers
- Real update/version distribution
- Notifications
- Expanded automated tests
- Production deployment configuration
